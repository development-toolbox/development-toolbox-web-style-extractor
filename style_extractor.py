#!/usr/bin/env python3
"""
Web Style Extractor v2.0 - Plugin-based architecture
Extract colors, fonts, and design systems from websites
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from urllib.parse import urlparse
import yaml
from typing import Optional

# Import our new plugin system
from core.engine import WebStyleExtractorEngine
from version import get_display_name, get_version_string, __version__


def setup_logging(debug: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if debug else logging.INFO
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Suppress noisy third-party loggers
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)

def create_output_directory(url: str, project_name: Optional[str] = None) -> str:
    """Create output directory for the project"""
    if project_name:
        dir_name = project_name
    else:
        # Create directory name from URL
        parsed = urlparse(url)
        dir_name = parsed.netloc.replace('www.', '')
        dir_name = parsed.netloc.replace('www.', '')

    # Ensure directory name is safe
    safe_dir_name = "".join(c for c in dir_name if c.isalnum() or c in '.-_')

    projects_dir = Path('projects')
    projects_dir.mkdir(exist_ok=True)

    output_path = projects_dir / safe_dir_name
    output_path.mkdir(exist_ok=True)

    return str(output_path)


def load_config() -> dict:
    """Load configuration from YAML files"""
    config = {}

    # Load plugin config
    plugins_config_path = 'config/plugins.yaml'
    if os.path.exists(plugins_config_path):
        with open(plugins_config_path, 'r') as f:
            config['plugins'] = yaml.safe_load(f)

    # Load settings config
    settings_config_path = 'config/settings.yaml'
    if os.path.exists(settings_config_path):
        with open(settings_config_path, 'r') as f:
            config['settings'] = yaml.safe_load(f)

    return config


def main():
    """Main entry point"""
    # Fix Windows console encoding for emojis (safer approach)
    if os.name == 'nt':  # Windows
        try:
            # Type-safe way to reconfigure stdout encoding
            if hasattr(sys.stdout, 'reconfigure') and callable(getattr(sys.stdout, 'reconfigure', None)):
                sys.stdout.reconfigure(encoding='utf-8', errors='replace')  # type: ignore
            elif hasattr(sys.stdout, 'buffer'):
                import io
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        except Exception:
            pass  # Continue with default encoding if this fails
            
    # Create extraction engine to get dynamic format info
    engine = WebStyleExtractorEngine()
    
    try:
        available_formats = engine.get_format_choices_for_cli()
        default_format = engine.get_default_format()
        format_descriptions = engine.get_format_descriptions_for_help()
    except Exception as e:
        # Fallback if plugin discovery fails
        print(f"Warning: Plugin discovery failed: {e}")
        available_formats = ['json']
        default_format = 'json'
        format_descriptions = "  json         💾 Structured JSON data"
    
    # Create argument parser with dynamic content
    parser = argparse.ArgumentParser(
        description='Extract style information from websites using a plugin-based architecture.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  %(prog)s https://example.com                    # {default_format} format (default)
  %(prog)s https://github.com -o {available_formats[0] if available_formats else 'json'}           # Short option format  
  %(prog)s https://example.com -o css            # CSS variables
  %(prog)s https://example.com -a                # All formats
  %(prog)s https://example.com -p "My Site"      # Custom project name
  %(prog)s https://example.com -a -p "GitHub Styles" # All formats with custom name

Available formats:
{format_descriptions}
        """)

    # Positional arguments
    parser.add_argument('url', help='Website URL to analyze')

    # Output options (dynamic from plugins)
    parser.add_argument('-o', '--output', 
                       choices=available_formats,
                       help=f'Output format (default: {default_format})')
    parser.add_argument('-a', '--all-formats', action='store_true',
                       help='Generate all available formats')
    parser.add_argument('-p', '--project-name',
                       help='Custom project name (default: derived from URL)')
    parser.add_argument('-f', '--output-file',
                       help='Custom output file name')

    # Debug options
    parser.add_argument('-d', '--debug', action='store_true',
                       help='Enable debug logging')
    parser.add_argument('-v', '--version', action='version',
                       version=f'{get_display_name()} {get_version_string()}')

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.debug)
    logger = logging.getLogger(__name__)

    # Load configuration
    config = load_config()

    # Use the already created engine
    # engine = WebStyleExtractorEngine()  # Already created above

    # Default to dynamic default format if no format specified
    if not args.output and not args.all_formats:
        args.output = default_format

    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url

    logger.info(f"🌐 Starting extraction for: {args.url}")
    logger.info(f"🔧 Using {get_display_name()} {get_version_string()}")

    # Determine which generators to enable
    if args.all_formats:
        enabled_generators = None  # Enable all available generators
        logger.info("📦 Generating ALL available formats")
    else:
        # Map format name to generator name (add _generator suffix)
        enabled_generators = [f"{args.output}_generator"]
        logger.info(f"📦 Generating format: {args.output}")
    
    # Always enable README generator for project documentation
    if enabled_generators is not None:
        enabled_generators.append("readme_generator")
        logger.info("📚 Adding README documentation generation")

    # Create output directory (enkelt)
    output_path = create_output_directory(args.url, args.project_name)

    logger.info(f"📁 Output directory: {output_path}")

    try:
        # Perform extraction (alla extractors, en generator)
        results = engine.extract(
            url=args.url,
            enabled_extractors=None,  # Alla extractors
            enabled_generators=enabled_generators,
            output_path=output_path
        )

        if not results:
            logger.error("❌ Extraction failed - no results returned")
            return 1

        # Save results
        extraction_results = results.get('extraction', {})
        generation_results = results.get('generation', {})

        # Generate output files
        total_files_generated = 0

        for generator_name, generator_result in generation_results.items():
            if generator_result and 'file' in generator_result:
                total_files_generated += 1
                logger.info(f"✅ Generated: {generator_result['file']}")

        # Generate metadata file
        metadata_path = os.path.join(output_path, 'metadata.txt')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write(f"Web Style Extractor v{__version__} - Extraction Report\n")
            f.write(f"{'=' * 60}\n\n")
            f.write(f"URL: {args.url}\n")
            f.write(f"Extracted at: {results.get('timestamp', 'Unknown')}\n")
            f.write(f"Output directory: {output_path}\n\n")

            f.write("Extractors used:\n")
            for extractor in results.get('metadata', {}).get('extractors_used', []):
                f.write(f"  • {extractor}\n")

            f.write("\nGenerators used:\n")
            for generator in results.get('metadata', {}).get('generators_used', []):
                f.write(f"  • {generator}\n")

            f.write(f"\nTotal files generated: {total_files_generated}\n")

            # Add summary statistics
            if 'color_extractor' in extraction_results:
                colors_count = extraction_results['color_extractor'].get('total_colors_found', 0)
                f.write(f"Colors extracted: {colors_count}\n")

            if 'font_extractor' in extraction_results:
                fonts_count = extraction_results['font_extractor'].get('total_fonts_found', 0)
                f.write(f"Fonts extracted: {fonts_count}\n")

        # Success message
        print(f"\n🎉 Extraction completed successfully!")
        print(f"📊 Generated {total_files_generated} files in: {output_path}")
        print(f"📄 See metadata.txt for detailed extraction report")

        if 'bookstack_generator' in generation_results:
            print(f"📚 BookStack theme ready! See README.md for installation instructions")

        return 0

    except KeyboardInterrupt:
        logger.info("⏹️  Extraction cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"❌ Extraction failed: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())