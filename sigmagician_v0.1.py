import os
import subprocess
import sys
import yaml
import pypandoc

def translate_sigma(sigma_file, backend):
    """Translate a Sigma rule into the chosen backend using sigma-cli.""" 
    try:
        result = subprocess.run(
            ["sigma", "convert", "-t", backend, sigma_file],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[!] Error while translating {sigma_file}: {e.stderr}")
        return None

def extract_metadata(sigma_file):
    """Extract metadata (title, description, tags) from a Sigma rule YAML file."""
    try:
        with open(sigma_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        title = data.get("title", "No title")
        description = data.get("description", "No description")
        tags = ", ".join(data.get("tags", [])) if data.get("tags") else "No tags"
        return title, description, tags
    except Exception as e:
        print(f"[!] Could not extract metadata from {sigma_file}: {e}")
        return "No title", "No description", "No tags"

def main():
    print("=== Sigma Rule Translator ===")

    # Step 1: Ask for Sigma rule file or directory
    sigma_path = input("Enter path to Sigma rule file or directory: ").strip()

    sigma_files = []
    if os.path.isfile(sigma_path):
        sigma_files = [sigma_path]
    elif os.path.isdir(sigma_path):
        for root, _, files in os.walk(sigma_path):
            for f in files:
                if f.endswith(".yml") or f.endswith(".yaml"):
                    sigma_files.append(os.path.join(root, f))
    else:
        print("[!] File or directory not found.")
        sys.exit(1)

    if not sigma_files:
        print("[!] No Sigma rule files found.")
        sys.exit(1)

    # Step 2: Ask which backend to translate to
    print("Select backend:")
    print("1. KQL (Azure Sentinel / Microsoft 365 Defender)")
    print("2. SPL (Splunk)")
    print("3. CarbonBlack")

    choice = input("Enter choice (1-3): ").strip()

    if choice == "1":
        backend = "kql"
    elif choice == "2":
        backend = "splunk"
    elif choice == "3":
        backend = "carbonblack"
    else:
        print("[!] Invalid choice.")
        sys.exit(1)

    # Step 3: Ask whether to merge queries
    merge_choice = input("Do you want to merge all translated queries into one hunting pack? (y/n): ").strip().lower()
    merge_queries = (merge_choice == "y")

    # Step 4: Perform translation for each file
    output_dir = os.path.join(os.getcwd(), f"sigma_translations_{backend}")
    os.makedirs(output_dir, exist_ok=True)

    merged_output_path = os.path.join(output_dir, f"hunting_pack_{backend}.md")
    merged_content = []
    toc_entries = []

    for sigma_file in sigma_files:
        print(f"\n[+] Translating: {sigma_file}")
        query = translate_sigma(sigma_file, backend)
        if query:
            base_name = os.path.splitext(os.path.basename(sigma_file))[0]
            output_file = os.path.join(output_dir, f"{base_name}_{backend}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(query)
            print(f"[+] Saved: {output_file}")

            if merge_queries:
                title, description, tags = extract_metadata(sigma_file)
                anchor = title.replace(" ", "-").lower()
                toc_entries.append(f"- [{title}](#{anchor})")
                merged_content.append(
                    f"# {title}\n\n**Description:** {description}\n\n**Tags:** {tags}\n\n" 
                    f"### Query from `{base_name}`\n\n````{backend}\n{query}\n````\n\n"
                )

    # Step 5: Save merged hunting pack with TOC if requested
    if merge_queries and merged_content:
        with open(merged_output_path, "w", encoding="utf-8") as f:
            f.write("# Hunting Pack\n\n")
            f.write("## Table of Contents\n\n")
            f.write("\n".join(toc_entries) + "\n\n")
            f.writelines(merged_content)
        print(f"\n[✓] Hunting pack with TOC created: {merged_output_path}")

        # Step 6: Ask if user wants PDF export
        pdf_choice = input("Do you want to export the hunting pack as PDF? (y/n): ").strip().lower()
        if pdf_choice == "y":
            pdf_output_path = merged_output_path.replace(".md", ".pdf")
            try:
                pypandoc.convert_text(
                    open(merged_output_path, "r", encoding="utf-8").read(),
                    "pdf",
                    format="md",
                    outputfile=pdf_output_path,
                    extra_args=['--standalone']
                )
                print(f"[✓] PDF export created: {pdf_output_path}")
            except Exception as e:
                print(f"[!] Failed to export PDF: {e}")

    print(f"\n[✓] All translations completed. Results saved in: {output_dir}")

if __name__ == "__main__":
    main()
