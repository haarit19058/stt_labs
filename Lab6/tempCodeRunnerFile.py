hart for unique CWE findings per tool
# unique_findings = df.groupby("Tool_name")["CWE_ID"].nunique().reset_index()
# plt.figure(figsize=(8, 6))
# sns.barplot(data=unique_findings, x="Tool_name", y="CWE_ID", palette="viridis")
# plt.title("Unique CWE Findings per Tool")
# plt.xlabel("Tool Name")
# plt.ylabel("Number of Unique CWE Findings")
# plt.savefig("unique_cwe_findings_per_tool.png")
# plt.show()
# print("Bar chart saved as 'unique_cwe_findings_per_tool.png'")


# # Heatmap for pairwise IoU matrix
# plt.figure(figsize=(8, 6))
# sns.heatmap(iou_matrix.astype(float), annot=True, cmap="YlGnBu", cbar_kws={'label': 'IoU'})
# plt.title("Pairwise IoU Matrix")
# plt.xlabel("Tool Name")
# plt.ylabel("Tool Name")
# plt.savefig("pairwise_iou_matrix.png")
# plt.show()
# print("Heatmap saved as 'pairwise_iou_matrix.png'")

# # Barchart for percentage of findings in CWE Top 25 per tool
# top25_percentage = []
# for tool in tools_list:
#     tool_data = df[df["Tool_name"] == tool]
#     total_findings = tool_data["Number_of_Findings"].sum()
#     top25_findings = tool_data[tool_data["Is_In_CWE_Top_25?"] == "YES"]["Number_of_Findings"].sum()
#     p_in_top25 = (top25_findings / total_findings * 100) if total_findings > 0 else 0
#     top25_percentage.append({"Tool_name": tool, "Percentage_in_CWE_Top_25": p_in_top25})

# # Convert to DataFrame for easier plotting
# top25_df = pd.DataFrame(top25_percentage)
# plt.figure(figsize=(8, 6))
# sns.barplot(data=top25_df, x="Tool_name", y="Percentage_in_CWE_Top_25", palette="magma")
# plt.title("Percentage of Findings in CWE Top 25 per Tool")
# plt.xlabel("Tool Name")
# plt.ylabel("Percentage in CWE Top 25 (%)")
# plt.ylim(0, 30)
# plt.savefig("percentage_in_cwe_top_25_per_tool.png")
# plt.show()
# print("Bar chart saved as 'percentage_in_cwe_top_25_per_tool.png'")


# # plot of cwe vs frequency for each tool in single plot per project
# for project in repo_list:
#     plt.figure(figsize=(12, 8))
#     project_data = df[df["Project_name"] == project]
#     sns.barplot(data=project_data, x="CWE_ID", y="Number_of_Findings", hue="Tool_name")
#     plt.title(f"CWE Findings per Tool for Project: {project}")
#     plt.xlabel("CWE ID")
#     plt.ylabel("Number of Findings")
#     plt.xticks(rotation=90)
#     plt.legend(title="Tool Name")
#     plt.tight_layout()
#     plt.savefig(f"cwe_findings_per_tool_{project}.png")
#     plt.show()
#     print(f"Bar chart saved as 'cwe_findings_per_tool_{project}.png'")