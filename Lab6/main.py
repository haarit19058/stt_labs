import pandas as pd
import json
import argparse
from collections import Counter
import os
import re

ggml_url = "https://github.com/ggml-org/ggml.git"
btop_url = "https://github.com/aristocratos/btop.git"
winget_url = "https://github.com/microsoft/winget-cli.git"

repo_list = ['ggml','btop','OpenCC']
tools_list = ['flawfinder','cppcheck','codeql']


cwe_top_25_ids = [
    "CWE-787",  # Out-of-bounds Write – Writing data past the allocated memory buffer.
    "CWE-79",   # Cross-site Scripting (XSS) – Improper input sanitization allowing script injection.
    "CWE-89",   # SQL Injection – Unvalidated input alters SQL queries.
    "CWE-416",  # Use After Free – Accessing memory after it has been freed.
    "CWE-78",   # OS Command Injection – Untrusted input used in system command execution.
    "CWE-20",   # Improper Input Validation – Failing to properly check input data.
    "CWE-125",  # Out-of-bounds Read – Reading memory beyond allocated buffer.
    "CWE-22",   # Path Traversal – Manipulating file paths to access restricted files.
    "CWE-352",  # Cross-Site Request Forgery (CSRF) – Unauthorized commands via authenticated user.
    "CWE-434",  # Unrestricted File Upload – Uploading malicious files to the server.
    "CWE-862",  # Missing Authorization – Access control not enforced for a resource.
    "CWE-476",  # NULL Pointer Dereference – Dereferencing a pointer that is NULL.
    "CWE-287",  # Improper Authentication – Weak or missing identity verification.
    "CWE-190",  # Integer Overflow or Wraparound – Arithmetic exceeds numeric bounds.
    "CWE-502",  # Deserialization of Untrusted Data – Executing malicious serialized data.
    "CWE-77",   # Command Injection – Improper neutralization of shell metacharacters.
    "CWE-119",  # Buffer Overflow – Accessing memory outside intended bounds.
    "CWE-798",  # Hard-coded Credentials – Embedded passwords or keys in code.
    "CWE-918",  # Server-Side Request Forgery (SSRF) – Server makes unintended external requests.
    "CWE-306",  # Missing Authentication for Critical Function – No login check on sensitive ops.
    "CWE-362",  # Race Condition – Concurrent actions cause inconsistent program state.
    "CWE-269",  # Improper Privilege Management – Wrongly assigning or using user privileges.
    "CWE-94",   # Code Injection – Executing attacker-controlled code.
    "CWE-863",  # Incorrect Authorization – Misapplied access control allowing privilege abuse.
    "CWE-276",  # Incorrect Default Permissions – Insecure default file or resource permissions.
]



# ------------   parsing xml to csv for cppcheck --------------
import xml.etree.ElementTree as ET
import csv

def parse_xml(xml_file,csv_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # CSV header
        writer.writerow(['File', 'Line', 'Severity', 'ID', 'Message', 'Verbose', 'CWE', 'Column', 'Info', 'Symbol'])

        for error in root.findall(".//error"):
            eid = error.attrib.get('id', '')
            severity = error.attrib.get('severity', '')
            msg = error.attrib.get('msg', '')
            verbose = error.attrib.get('verbose', '')
            cwe = error.attrib.get('cwe', '')

            # Multiple locations
            for loc in error.findall('location'):
                file = loc.attrib.get('file', '')
                line = loc.attrib.get('line', '')
                column = loc.attrib.get('column', '')
                info = loc.attrib.get('info', '')  # optional
                symbol = error.findtext('symbol', '')  # optional
                writer.writerow([file, line, severity, eid, msg, verbose, cwe, column, info, symbol])

    print(f"CSV report generated: {csv_file}")
    return

for name in repo_list:
    parse_xml(f"cppcheck_{name}.xml",f"cppcheck_{name}.csv")



df = pd.DataFrame(columns=["Project_name", "Tool_name", "CWE_ID", "Number_of_Findings", "Is_In_CWE_Top_25?"])


# ---------------- process flawfinder data -----------------------
for project in repo_list:
    project_data = pd.read_csv(f"flawfinder_{project}.csv")
    
    # split comma-separated CWEs into separate rows
    project_data["CWEs"] = project_data["CWEs"].astype(str).str.split(",")
    project_data = project_data.explode("CWEs")
    project_data["CWEs"] = project_data["CWEs"].str.strip()
    
    # count findings per CWE
    counts = project_data.groupby("CWEs").size().reset_index(name="Number_of_Findings")
    
    for _, row in counts.iterrows():
        cwe_id = row["CWEs"]
        nfindings = row["Number_of_Findings"]
        topcwe = "YES" if cwe_id in cwe_top_25_ids else "NO"
        
        df = pd.concat([df, pd.DataFrame([{
            "Project_name": project,
            "Tool_name": "flawfinder",
            "CWE_ID": cwe_id,
            "Number_of_Findings": nfindings,
            "Is_In_CWE_Top_25?": topcwe
        }])], ignore_index=True)




# -------------------- process cppcheck data -----------------------
for project in repo_list:
    project_data = pd.read_csv(f"cppcheck_{project}.csv")
    counts = project_data.groupby("CWE").size().reset_index(name="Number_of_Findings")
    
    for _, row in counts.iterrows():
        cwe_id = f"CWE-{int(row["CWE"])}"
        nfindings = row["Number_of_Findings"]
        topcwe = "YES" if cwe_id in cwe_top_25_ids else "NO"
        
        df = pd.concat([df, pd.DataFrame([{
            "Project_name": project,
            "Tool_name": "cppcheck",
            "CWE_ID": cwe_id,
            "Number_of_Findings": int(nfindings),
            "Is_In_CWE_Top_25?": topcwe
        }])], ignore_index=True)










# --------------------- Processing code ql data -----------------------


def extract_cwe_from_tags(rule):
    """
    Extracts CWE identifiers from the 'tags' property of a rule object.
    Handles various common formats like 'CWE-123' or 'external/cwe/cwe-123'.
    """
    if not rule:
        return []

    tags = rule.get('properties', {}).get('tags', [])
    if not tags:
        return []

    cwe_ids = []
    # This regex finds patterns like 'cwe-123' or 'CWE-789' inside the tags.
    cwe_pattern = re.compile(r'cwe-(\d+)', re.IGNORECASE)

    for tag in tags:
        match = cwe_pattern.search(tag)
        if match:
            # Format it consistently as CWE-XXX
            cwe_id = f"CWE-{match.group(1)}"
            cwe_ids.append(cwe_id)
            
    return cwe_ids

def analyze_sarif(file_path):
    """
    Parses a SARIF file, counts CWEs, and returns the counts.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sarif_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{file_path}'. The file may be corrupted.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return None

    cwe_counter = Counter()

    for run in sarif_data.get('runs', []):
        results = run.get('results', [])
        
        # Create a quick-lookup map from ruleId to the full rule object.
        # This is more efficient than searching the rules list for every result.
        rules = run.get('tool', {}).get('driver', {}).get('rules', [])
        rule_map = {rule['id']: rule for rule in rules}

        for result in results:
            rule_id = result.get('ruleId')
            if not rule_id:
                continue

            rule = rule_map.get(rule_id)
            if not rule:
                continue

            # Extract one or more CWEs from the rule's tags
            cwe_ids = extract_cwe_from_tags(rule)
            for cwe_id in cwe_ids:
                cwe_counter[cwe_id] += 1
    
    return cwe_counter

#   save sariff to csv for assignment
for project in repo_list:
    sarif_file = f"codeql_{project}.sarif"
    cwe_counts = analyze_sarif(sarif_file)
    
    if cwe_counts is None:
        continue  # Skip to the next project if there was an error

    with open(f"codeql_{project}.csv", 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['CWE_ID', 'Number_of_Findings']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for cwe_id, nfindings in cwe_counts.items():
            writer.writerow({'CWE_ID': cwe_id, 'Number_of_Findings': nfindings})

for project in repo_list:
    sarif_file = f"codeql_{project}.sarif"
    cwe_counts = analyze_sarif(sarif_file)
    
    if cwe_counts is None:
        continue  # Skip to the next project if there was an error

    for cwe_id, nfindings in cwe_counts.items():
        topcwe = "YES" if cwe_id in cwe_top_25_ids else "NO"
        
        df = pd.concat([df, pd.DataFrame([{
            "Project_name": project,
            "Tool_name": "codeql",
            "CWE_ID": cwe_id,
            "Number_of_Findings": nfindings,
            "Is_In_CWE_Top_25?": topcwe
        }])], ignore_index=True)





# ---------------------- Final report generation -----------------------

print(df)
df.to_csv("final_report.csv", index=False)
print("Final report generated: final_report.csv")















# -------------------- tool level analysis -----------------------

# calculate unique findings
print("\nUnique CWE Findings per Tool:\n")
for tool in tools_list:
    unique_findings = df[df["Tool_name"] == tool]["CWE_ID"].nunique()
    print(f"Tool:{tool} - Unique CWE Findings: \t{unique_findings}\t")

# calculate percentage in top 25
print("\n\nTool Level Analysis:\n")
for tool in tools_list:
    tool_data = df[df["Tool_name"] == tool]
    total_findings = tool_data["Number_of_Findings"].sum()
    top25_findings = tool_data[tool_data["Is_In_CWE_Top_25?"] == "YES"]["Number_of_Findings"].sum()
    p_in_top25 = (top25_findings / total_findings * 100) if total_findings > 0 else 0
    print(f"Tool: {tool}")
    print(f"  Total Findings: \t\t{total_findings}")
    print(f"  Findings in CWE Top 25: \t{top25_findings}")
    print(f"  Percentage in CWE Top 25: \t{p_in_top25:.2f}%")
    print()


#  ------------------ creating a pairwise IoU matrix -----------------------
iou_matrix = pd.DataFrame(index=tools_list, columns=tools_list)

for tool1 in tools_list:
    for tool2 in tools_list:
        if tool1 == tool2:
            continue
        # Calculate IoU for tool1 and tool2
        intersection = df[(df["Tool_name"] == tool1) & (df["CWE_ID"].isin(df[df["Tool_name"] == tool2]["CWE_ID"]))].shape[0]
        union = df[(df["Tool_name"] == tool1) | (df["Tool_name"] == tool2)].shape[0]
        iou = intersection / union if union > 0 else 0
        iou_matrix.loc[tool1, tool2] = iou
print("\nPairwise IoU Matrix:\n")
print(iou_matrix)




# ------------------- plotting graphs -----------------------
import matplotlib.pyplot as plt
import seaborn as sns

# # Bar chart for unique CWE findings per tool
unique_findings = df.groupby("Tool_name")["CWE_ID"].nunique().reset_index()
plt.figure(figsize=(8, 6))
sns.barplot(data=unique_findings, x="Tool_name", y="CWE_ID", palette="viridis")
plt.title("Unique CWE Findings per Tool")
plt.xlabel("Tool Name")
plt.ylabel("Number of Unique CWE Findings")
plt.savefig("unique_cwe_findings_per_tool.png")
plt.show()
print("Bar chart saved as 'unique_cwe_findings_per_tool.png'")


# # Heatmap for pairwise IoU matrix
plt.figure(figsize=(8, 6))
sns.heatmap(iou_matrix.astype(float), annot=True, cmap="YlGnBu", cbar_kws={'label': 'IoU'})
plt.title("Pairwise IoU Matrix")
plt.xlabel("Tool Name")
plt.ylabel("Tool Name")
plt.savefig("pairwise_iou_matrix.png")
plt.show()
print("Heatmap saved as 'pairwise_iou_matrix.png'")

# # Barchart for percentage of findings in CWE Top 25 per tool
top25_percentage = []
for tool in tools_list:
    tool_data = df[df["Tool_name"] == tool]
    total_findings = tool_data["Number_of_Findings"].sum()
    top25_findings = tool_data[tool_data["Is_In_CWE_Top_25?"] == "YES"]["Number_of_Findings"].sum()
    p_in_top25 = (top25_findings / total_findings * 100) if total_findings > 0 else 0
    top25_percentage.append({"Tool_name": tool, "Percentage_in_CWE_Top_25": p_in_top25})

# # Convert to DataFrame for easier plotting
top25_df = pd.DataFrame(top25_percentage)
plt.figure(figsize=(8, 6))
sns.barplot(data=top25_df, x="Tool_name", y="Percentage_in_CWE_Top_25", palette="magma")
plt.title("Percentage of Findings in CWE Top 25 per Tool")
plt.xlabel("Tool Name")
plt.ylabel("Percentage in CWE Top 25 (%)")
plt.ylim(0, 30)
plt.savefig("percentage_in_cwe_top_25_per_tool.png")
plt.show()
print("Bar chart saved as 'percentage_in_cwe_top_25_per_tool.png'")


# plot of cwe vs frequency for each tool in single plot per project
for project in repo_list:
    plt.figure(figsize=(12, 8))
    project_data = df[df["Project_name"] == project]
    sns.barplot(data=project_data, x="CWE_ID", y="Number_of_Findings", hue="Tool_name")
    plt.title(f"CWE Findings per Tool for Project: {project}")
    plt.xlabel("CWE ID")
    plt.ylabel("Number of Findings")
    plt.xticks(rotation=90)
    plt.legend(title="Tool Name")
    plt.tight_layout()
    plt.savefig(f"cwe_findings_per_tool_{project}.png")
    plt.show()
    print(f"Bar chart saved as 'cwe_findings_per_tool_{project}.png'")


# plotting pie chart for each tool showing distribution of findings across projects
for tool in tools_list:
    plt.figure(figsize=(8, 8))
    tool_data = df[df["Tool_name"] == tool]
    project_counts = tool_data.groupby("Project_name")["Number_of_Findings"].sum().reset_index()
    plt.pie(project_counts["Number_of_Findings"], labels=project_counts["Project_name"], autopct='%1.1f%%', startangle=140)
    plt.title(f"Distribution of Findings across Projects for Tool: {tool}")
    plt.savefig(f"distribution_of_findings_{tool}.png")
    plt.show()
    print(f"Pie chart saved as 'distribution_of_findings_{tool}.png'")



# plotting pie chart for each CWE showing distribution of findings across projects
# for cwe in df["CWE_ID"].unique():
#     plt.figure(figsize=(8, 8))
#     cwe_data = df[df["CWE_ID"] == cwe]
#     project_counts = cwe_data.groupby("Project_name")["Number_of_Findings"].sum().reset_index()
#     plt.pie(project_counts["Number_of_Findings"], labels=project_counts["Project_name"], autopct='%1.1f%%', startangle=140)
#     plt.title(f"Distribution of Findings across Projects for CWE: {cwe}")
#     # plt.savefig(f"distribution_of_findings_{cwe}.png")
#     plt.show()
#     # print(f"Pie chart saved as 'distribution_of_findings_{cwe}.png'")

# plotting pie chart for CWE showing distribution of findings across projects

for project in repo_list:
    plt.figure(figsize=(8, 8))
    project_data = df[df["Project_name"] == project]
    cwe_counts = project_data.groupby("CWE_ID")["Number_of_Findings"].sum().reset_index()
    plt.pie(cwe_counts["Number_of_Findings"], labels=cwe_counts["CWE_ID"], autopct='%1.1f%%', startangle=140)
    plt.title(f"Distribution of Findings across CWEs for Project: {project}")
    plt.savefig(f"distribution_of_findings_across_cwes_{project}.png")
    plt.show()
    print(f"Pie chart saved as 'distribution_of_findings_across_cwes_{project}.png'")


























'''


Project: btop

Flawfinder

CWE-120 — 80 occurrences (combined from 67 + 13) — Buffer Copy without Checking Size of Input (classic buffer overflow) — writing more data into a buffer than it can hold. ([CWE][1])
CWE-362 — 31 occurrences — Race condition / concurrent execution using shared resources causing inconsistent program state. ([CWE][2])

Cppcheck

CWE-398 — 47 occurrences — Indicator of Poor Code Quality (“code smells” that make software harder to maintain and more likely to contain issues).
CWE-561 — 46 occurrences — Dead Code — code that is never executed.
CWE-758 — 8 occurrences — Reliance on Undefined, Unspecified, or Implementation-Defined Behavior — code depends on behavior not guaranteed by the language or platform. ([Security Database][3])

CodeQL

CWE-367 — 1 occurrence — Time-of-check Time-of-use (TOCTOU) race condition: resource state changes between check and use.

---

Project: ggml

Cppcheck

CWE-398 — 2,488 occurrences — Indicator of Poor Code Quality (“code smells”).
CWE-561 — 471 occurrences — Dead Code.

Flawfinder

CWE-120 — 626 occurrences — Buffer Copy without Checking Size of Input (classic buffer overflow). ([CWE][1])
CWE-20 — 232 occurrences — Improper Input Validation — failing to validate or sanitize input before use. ([CWE][4])
CWE-807 — 43 occurrences — Reliance on Untrusted Inputs in a Security Decision — making security decisions based on inputs that can be tampered with. ([CWE][5])
CWE-190 — 40 occurrences — Integer Overflow or Wraparound — arithmetic exceeds numeric bounds, causing incorrect results or memory issues. ([CWE][6])

CodeQL

CWE-190 — 38 occurrences — Integer Overflow or Wraparound. ([CWE][6])
CWE-191 — 25 occurrences — Integer Underflow (wrap or wraparound). ([CWE][7])

---

Project: OpenCC

Flawfinder

CWE-120 — 99 occurrences — Buffer Copy without Checking Size of Input (classic buffer overflow). ([CWE][1])
CWE-20 — 55 occurrences — Improper Input Validation. ([CWE][4])
CWE-362 — 34 occurrences — Race condition / concurrent execution issues. ([CWE][2])

Cppcheck

CWE-398 — 232 occurrences — Indicator of Poor Code Quality (“code smells”).
CWE-561 — 65 occurrences — Dead Code.
CWE-628 — 36 occurrences — Function Call with Incorrectly Specified Arguments — calling a function with arguments that are not correctly specified, producing incorrect behavior. ([Backslash Security][8])

CodeQL

CWE-29 — 14 occurrences — (External Control of System or Configuration Settings / input used to influence system behavior) — review tool output for exact sub-type.
CWE-23 — 4 occurrences — Relative Path Traversal / External Control of File Name or Pathname.
CWE-190 — 4 occurrences — Integer Overflow or Wraparound. ([CWE][6])
CWE-73 — 4 occurrences — External Control of File Name or Path (path/filename provided by external input).



'''