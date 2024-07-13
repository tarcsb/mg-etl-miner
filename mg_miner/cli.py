import argparse
import logging
from mg_miner.core.file_collector import FileCollector
from mg_miner.core.component_detector import ComponentDetector
from mg_miner.core.redactor import Redactor
from mg_miner.core.summary_creator import SummaryCreator

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(description="mg-miner CLI")
    subparsers = parser.add_subparsers(dest="command")

    # File collector command
    parser_collect = subparsers.add_parser('collect', help="Collect files")
    parser_collect.add_argument('config_path', type=str, help="Path to the configuration file for file collection")

    # Component detector command
    parser_detect = subparsers.add_parser('detect', help="Detect components")
    parser_detect.add_argument('output_dir', type=str, help="Output directory")

    # Redactor command
    parser_redact = subparsers.add_parser('redact', help="Redact sensitive information")
    parser_redact.add_argument('output_dir', type=str, help="Output directory")
    parser_redact.add_argument('compliance_standards', type=str, nargs='+', help="List of compliance standards to apply for redaction")

    # Summary creator command
    parser_summary = subparsers.add_parser('summary', help="Create summary")
    parser_summary.add_argument('output_dir', type=str, help="Output directory")
    parser_summary.add_argument('theme', type=str, help="Theme for the summary")

    args = parser.parse_args()

    if args.command == "collect":
        collector = FileCollector.from_config(args.config_path)
        collector.collect_files()
    elif args.command == "detect":
        detector = ComponentDetector(output_dir=args.output_dir, silent=False)
        detector.detect_components()
    elif args.command == "redact":
        redactor = Redactor(output_dir=args.output_dir, compliance_standards=args.compliance_standards, silent=False)
        redactor.redact_sensitive_info()
    elif args.command == "summary":
        creator = SummaryCreator(output_dir=args.output_dir, silent=False, theme=args.theme)
        creator.create_summary()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
