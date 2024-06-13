# import streamlit as st
# import pandas as pd
# from company_specific_functions import *
# from general_functions import *
# from harm_specific_functions import *
# from functions import *
import pickle
import zipfile
from pathlib import Path
from collections import defaultdict
import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


# def extract_all_zip(folder_path):
#     folder = Path(folder_path)
#     for zip_file in folder.glob("*.zip"):
#         # Open the zip file in read mode
#         with zipfile.ZipFile(zip_file, 'r') as archive:
#             for member in archive.namelist():
#                 # Extract each file from the zip without its internal path
#                 archive.extract(member, path=folder)
#                 print(f"Extracted '{member}' from '{zip_file.name}'.")
#         os.remove(zip_file)


# def nested_dic():
#     return defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int)))))


# # directory = r"/home/tdi/Downloads/sor-global-2024-06-03-full"
# # extract_all_zip(directory)
# #
# # print("Processing FILE")
# # csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
# #
# # dataset = nested_dic()
# #
# # for file in csv_files:
# #     print("Merging:", file)  # Print the file being merged
# #     df = pd.read_csv(os.path.join(directory, file), low_memory=False)
# #     List_of_companies = df['platform_name'].unique()
# #     List_of_harms = df['category'].unique()
# #     List_of_content_type = df['content_type'].unique()
# #     List_of_moderation_action = df['decision_visibility'].unique()
# #     List_of_automation_status = df['automated_decision'].unique()
# #     for company in List_of_companies:
# #         company_df = df[df['platform_name'] == company]
# #         for harm in List_of_harms:
# #             harm_df = company_df[company_df['category'] == harm]
# #             for content_type in List_of_content_type:
# #                 content_type_df = harm_df[harm_df['content_type'] == content_type]
# #                 for moderation_action in List_of_moderation_action:
# #                     moderation_action_df = content_type_df[content_type_df['decision_visibility'] == moderation_action]
# #                     for automation_status in List_of_automation_status:
# #                         count = (moderation_action_df['automated_decision'] == automation_status).sum()
# #                         # if count > 0:
# #                         #     print('###Numebr', count)
# #                         dataset[company][harm][content_type][moderation_action][automation_status] += count
# #
# #     print("Processing Complete")
# #
# #
# # def convert_to_dict(d):
# #     """ Recursively converts a defaultdict to a regular dictionary. """
# #     if isinstance(d, defaultdict):
# #         d = {k: convert_to_dict(v) for k, v in d.items()}
# #     return d
# #
# #
# # dataset_dict = convert_to_dict(dataset)
# #
# # with open('data_ACC.pkl', 'wb') as f:
# #     # Pickle the dictionary and write to file
# #     pickle.dump(dataset_dict, f)


file_path = 'data_ACC.pkl'

# Open the file in binary read mode
with open(file_path, 'rb') as f:
    # Load the pickled data back into a dictionary variable
    data_ACC = pickle.load(f)

# Assuming data_ACC is the loaded dictionary from the pickle file
List_of_companies = list(data_ACC.keys())
harm_dic = data_ACC[List_of_companies[0]]
List_of_harms = list(harm_dic.keys())
content_dic = harm_dic[List_of_harms[0]]
List_of_content_type = list(content_dic.keys())
action_dic = content_dic[List_of_content_type[0]]
List_of_moderation_action = list(action_dic.keys())
automation_dic = action_dic[List_of_moderation_action[0]]
List_of_automation_status = list(automation_dic.keys())


######### Data General plot - Total number of Moderation Actions per Company
# def plot_company_data(data):
#     """ Sum all numbers for a certain company key and plot the results as both a table and a bar chart. """
#     def sum_company(data, company):
#         """ Sum all numbers for a certain company key """
#         total_sum = 0
#         for harm in data[company].values():
#             for content_type in harm.values():
#                 for moderation_action in content_type.values():
#                     for automation_status in moderation_action.values():
#                         total_sum += automation_status
#         return total_sum

#     company_data = {'Company': [], 'N# Actions': []}
#     for company in List_of_companies:
#         num_actions = sum_company(data, company)
#         company_data['Company'].append(company)
#         company_data['N# Actions'].append(num_actions)

#     df_company = pd.DataFrame(company_data).dropna()

#     # Plotting the table and graph
#     fig, ax = plt.subplots(2, figsize=(10, 12))

#     # Table
#     ax[0].axis('tight')
#     ax[0].axis('off')
#     table = ax[0].table(cellText=df_company.values, colLabels=df_company.columns, cellLoc='center', loc='center')

#     # Bar chart
#     df_company.plot(kind='bar', x='Company', y='N# Actions', ax=ax[1])
#     ax[1].set_xlabel('Company')
#     ax[1].set_ylabel('Total Number of Actions')
#     ax[1].set_title('Total Number of Actions per Company')

#     plt.tight_layout()
#     return fig


######### Data General plot - Total number of Moderation Actions per Harm

# def sum_harm_and_plot(data):
#     """ 
#     Sum all numbers for each harm type across all companies and plot the results as both a table and a bar chart. 
#     """
#     harm_totals = {}
#     for company in data.values():
#         for harm, harm_data in company.items():
#             if harm not in harm_totals:
#                 harm_totals[harm] = 0
#             for content_type in harm_data.values():
#                 for moderation_action in content_type.values():
#                     for automation_status in moderation_action.values():
#                         harm_totals[harm] += automation_status
    
#     # Create DataFrame from harm totals
#     harm_data = {'Harm': list(harm_totals.keys()), 'N# Actions': list(harm_totals.values())}
#     df_harm = pd.DataFrame(harm_data).dropna()

#     # Plotting the table and graph
#     fig, ax = plt.subplots(2, figsize=(10, 12))

#     # Table
#     ax[0].axis('tight')
#     ax[0].axis('off')
#     table = ax[0].table(cellText=df_harm.values, colLabels=df_harm.columns, cellLoc='center', loc='center')

#     # Bar chart
#     df_harm.plot(kind='bar', x='Harm', y='N# Actions', ax=ax[1])
#     ax[1].set_xlabel('Harm')
#     ax[1].set_ylabel('Total Number of Actions')
#     ax[1].set_title('Total Number of Actions per Harm')

#     plt.tight_layout()
#     return fig




######### Data General plot - Total number of Moderation Actions per Type of Content
def plot_content_type_table(data, company, harm):
    """Sum all numbers for each content type for a specific company and harm and plot as a table"""
    content_type_totals = {}

    if company in data:
        company_data = data[company]
        if harm in company_data:
            harm_data = company_data[harm]
            for content_type, content_data in harm_data.items():
                if content_type not in content_type_totals:
                    content_type_totals[content_type] = 0
                for moderation_action in content_data.values():
                    for automation_status in moderation_action.values():
                        content_type_totals[content_type] += automation_status
        else:
            print(f"No data found for harm: {harm}")
            return None
    else:
        print(f"No data found for company: {company}")
        return None

    content_type_data = {
        'Company': [company] * len(content_type_totals),
        'Harm': [harm] * len(content_type_totals),
        'Content Type': list(content_type_totals.keys()),
        'N# Actions': list(content_type_totals.values())
    }
    df_content_type = pd.DataFrame(content_type_data).dropna()


    category_descriptions = {
        'STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE': 'PLATFORM SCOPE',
        'STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS': 'GDPR VIOLATION',
        'STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT': 'PORN/SEX CONTENT',
        'STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH': 'ILLEGAL/HARMFULL SPEECH',
        'STATEMENT_CATEGORY_VIOLENCE': 'VIOLENCE',
        'STATEMENT_CATEGORY_SCAMS_AND_FRAUD': 'SCAMS/FRAUD',
        'STATEMENT_CATEGORY_UNSAFE_AND_ILLEGAL_PRODUCTS': 'ILLEGAL PRODUCTS',
        'STATEMENT_CATEGORY_NON_CONSENSUAL_BEHAVIOUR': 'NON CONSENSUAL BEHAVIOUR',
        'STATEMENT_CATEGORY_PROTECTION_OF_MINORS': 'PROTECT MINORS',
        'STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS': 'COPYRIGHT',
        'STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS': 'NEGATIVE EFFECTS ELECTIONS',
        'STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY': 'RISK PUBLIC SECURITY',
        'STATEMENT_CATEGORY_ANIMAL_WELFARE': 'ANIMAL WELFARE',
        'STATEMENT_CATEGORY_SELF_HARM': 'SELF HARM'
    }

    content_type_descriptions = {
        '["CONTENT_TYPE_OTHER"]': 'OTHER',
        '["CONTENT_TYPE_SYNTHETIC_MEDIA"]': 'SYNTHETIC MEDIA',
        '["CONTENT_TYPE_IMAGE"]': 'IMAGE',
        '["CONTENT_TYPE_TEXT"]': 'TEXT',
        '["CONTENT_TYPE_VIDEO"]': 'VIDEO',
        '["CONTENT_TYPE_PRODUCT"]': 'PRODUCT',
        '["CONTENT_TYPE_APP"]': 'APP',
        '["CONTENT_TYPE_AUDIO"]': 'AUDIO',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT"]': 'IMAGE/TEXT',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'IMAGE/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_TEXT"],"CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO/IMAGE',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_VIDEO"]': 'AUDIO/IMAGE/VIDEO'
    }

    df_content_type['Harm'] = df_content_type['Harm'].map(category_descriptions)
    df_content_type['Content Type'] = df_content_type['Content Type'].map(content_type_descriptions)

    # Display the DataFrame as a table
    print(df_content_type)

    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_content_type.values, colLabels=df_content_type.columns, cellLoc='center', loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    plt.show()
    return fig



######### Data General plot - Total number of Moderation Actions per Type of Moderation Actions

def plot_moderation_action_table(data, company, harm):
    """Sum all numbers for each moderation action for a specific company and harm and plot as a table"""
    moderation_action_totals = {}

    if company in data:
        company_data = data[company]
        if harm in company_data:
            harm_data = company_data[harm]
            for content_type in harm_data.values():
                for moderation_action, action_data in content_type.items():
                    if moderation_action not in moderation_action_totals:
                        moderation_action_totals[moderation_action] = 0
                    for automation_status in action_data.values():
                        moderation_action_totals[moderation_action] += automation_status
        else:
            print(f"No data found for harm: {harm}")
            return None
    else:
        print(f"No data found for company: {company}")
        return None

    moderation_action_data = {
        'Company': [company] * len(moderation_action_totals),
        'Harm': [harm] * len(moderation_action_totals),
        'Moderation Action': list(moderation_action_totals.keys()),
        'N# Actions': list(moderation_action_totals.values())
    }
    df_moderation_action = pd.DataFrame(moderation_action_data).dropna()


    category_descriptions = {
        'STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE': 'PLATFORM SCOPE',
        'STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS': 'GDPR VIOLATION',
        'STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT': 'PORN/SEX CONTENT',
        'STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH': 'ILLEGAL/HARMFULL SPEECH',
        'STATEMENT_CATEGORY_VIOLENCE': 'VIOLENCE',
        'STATEMENT_CATEGORY_SCAMS_AND_FRAUD': 'SCAMS/FRAUD',
        'STATEMENT_CATEGORY_UNSAFE_AND_ILLEGAL_PRODUCTS': 'ILLEGAL PRODUCTS',
        'STATEMENT_CATEGORY_NON_CONSENSUAL_BEHAVIOUR': 'NON CONSENSUAL BEHAVIOUR',
        'STATEMENT_CATEGORY_PROTECTION_OF_MINORS': 'PROTECT MINORS',
        'STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS': 'COPYRIGHT',
        'STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS': 'NEGATIVE EFFECTS ELECTIONS',
        'STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY': 'RISK PUBLIC SECURITY',
        'STATEMENT_CATEGORY_ANIMAL_WELFARE': 'ANIMAL WELFARE',
        'STATEMENT_CATEGORY_SELF_HARM': 'SELF HARM'
    }

    visibility_descriptions = {
    '["DECISION_VISIBILITY_CONTENT_REMOVED"]': 'REMOVED',
    '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED","DECISION_VISIBILITY_CONTENT_REMOVED"]': 'RESTRICTED/REMOVED',
    '["DECISION_VISIBILITY_CONTENT_REMOVED","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'REMOVED/AGE RESTRICTED',
    '["DECISION_VISIBILITY_OTHER","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'OTHER/AGE RESTRICTED',
    '["DECISION_VISIBILITY_CONTENT_LABELLED"]': 'LABELLED',
    '["DECISION_VISIBILITY_OTHER"]': 'OTHER',
    '["DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'AGE RESTRICTED',
    '["DECISION_VISIBILITY_CONTENT_DISABLED"]': 'DISABLED',
    '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED"]': 'INTERACTION RESTRICTED',
    '[]': 'NOT DEFINED',
    '["DECISION_VISIBILITY_CONTENT_DEMOTED"]': 'DEMOTED'

    }

    df_moderation_action['Harm'] = df_moderation_action['Harm'].map(category_descriptions)
    df_moderation_action['Moderation Action'] = df_moderation_action['Moderation Action'].map(visibility_descriptions)




    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_moderation_action.values, colLabels=df_moderation_action.columns, cellLoc='center', loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    plt.show()
    return fig


######### Data General plot - Total number of AUTOMATION Actions per Type of Moderation

def plot_automation_status_table(data, company, harm):
    """Sum all numbers for each automation status for a specific company and harm and plot as a table"""
    automation_status_totals = {}

    if company in data:
        company_data = data[company]
        if harm in company_data:
            harm_data = company_data[harm]
            for content_type in harm_data.values():
                for moderation_action in content_type.values():
                    for automation_status, count in moderation_action.items():
                        if automation_status not in automation_status_totals:
                            automation_status_totals[automation_status] = 0
                        automation_status_totals[automation_status] += count
        else:
            print(f"No data found for harm: {harm}")
            return None
    else:
        print(f"No data found for company: {company}")
        return None

    automation_status_data = {
        'Company': [company] * len(automation_status_totals),
        'Harm': [harm] * len(automation_status_totals),
        'Automation Status': list(automation_status_totals.keys()),
        'N# Actions': list(automation_status_totals.values())
    }
    df_automation_status = pd.DataFrame(automation_status_data).dropna()

    category_descriptions = {
        'STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE': 'PLATFORM SCOPE',
        'STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS': 'GDPR VIOLATION',
        'STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT': 'PORN/SEX CONTENT',
        'STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH': 'ILLEGAL/HARMFULL SPEECH',
        'STATEMENT_CATEGORY_VIOLENCE': 'VIOLENCE',
        'STATEMENT_CATEGORY_SCAMS_AND_FRAUD': 'SCAMS/FRAUD',
        'STATEMENT_CATEGORY_UNSAFE_AND_ILLEGAL_PRODUCTS': 'ILLEGAL PRODUCTS',
        'STATEMENT_CATEGORY_NON_CONSENSUAL_BEHAVIOUR': 'NON CONSENSUAL BEHAVIOUR',
        'STATEMENT_CATEGORY_PROTECTION_OF_MINORS': 'PROTECT MINORS',
        'STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS': 'COPYRIGHT',
        'STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS': 'NEGATIVE EFFECTS ELECTIONS',
        'STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY': 'RISK PUBLIC SECURITY',
        'STATEMENT_CATEGORY_ANIMAL_WELFARE': 'ANIMAL WELFARE',
        'STATEMENT_CATEGORY_SELF_HARM': 'SELF HARM'
    }

    automated_decision_cleaned = {
            'AUTOMATED_DECISION_FULLY': 'Fully Automated',
            'AUTOMATED_DECISION_NOT_AUTOMATED': 'Not Automated',
            'AUTOMATED_DECISION_PARTIALLY': 'Partially automated',
    }


    df_automation_status['Automation Status'] = df_automation_status['Automation Status'].map(automated_decision_cleaned)
    df_automation_status['Harm'] = df_automation_status['Harm'].map(category_descriptions)



    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_automation_status.values, colLabels=df_automation_status.columns, cellLoc='center', loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    plt.show()
    return fig



######### Data General plot - Number of reported Harms per Company IMPORTANT

#7
def plot_reports_per_harm_per_company(data, company, harm):
    """Sum all numbers for a specific harm for a specific company and plot as a table"""
    harm_totals_per_company = {}

    if company in data:
        harms = data[company]
        if harm in harms:
            harm_data = harms[harm]
            for content_type in harm_data.values():
                for moderation_action in content_type.values():
                    for count in moderation_action.values():
                        harm_totals_per_company[harm] = harm_totals_per_company.get(harm, 0) + count
        else:
            print(f"No data found for harm: {harm}")
            return None
    else:
        print(f"No data found for company: {company}")
        return None

    data_for_df = {'Company': [], 'Harm': [], 'N# Actions': []}
    for harm, total_actions in harm_totals_per_company.items():
        data_for_df['Company'].append(company)
        data_for_df['Harm'].append(harm)
        data_for_df['N# Actions'].append(total_actions)

    df_harm_per_company = pd.DataFrame(data_for_df).dropna()

    category_descriptions = {
        'STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE': 'PLATFORM SCOPE',
        'STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS': 'GDPR VIOLATION',
        'STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT': 'PORN/SEX CONTENT',
        'STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH': 'ILLEGAL/HARMFULL SPEECH',
        'STATEMENT_CATEGORY_VIOLENCE': 'VIOLENCE',
        'STATEMENT_CATEGORY_SCAMS_AND_FRAUD': 'SCAMS/FRAUD',
        'STATEMENT_CATEGORY_UNSAFE_AND_ILLEGAL_PRODUCTS': 'ILLEGAL PRODUCTS',
        'STATEMENT_CATEGORY_NON_CONSENSUAL_BEHAVIOUR': 'NON CONSENSUAL BEHAVIOUR',
        'STATEMENT_CATEGORY_PROTECTION_OF_MINORS': 'PROTECT MINORS',
        'STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS': 'COPYRIGHT',
        'STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS': 'NEGATIVE EFFECTS ELECTIONS',
        'STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY': 'RISK PUBLIC SECURITY',
        'STATEMENT_CATEGORY_ANIMAL_WELFARE': 'ANIMAL WELFARE',
        'STATEMENT_CATEGORY_SELF_HARM': 'SELF HARM'
    }

    df_harm_per_company['Harm'] = df_harm_per_company['Harm'].map(category_descriptions)

    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_harm_per_company.values, colLabels=df_harm_per_company.columns, cellLoc='center', loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    plt.show()
    return fig




######### Data General plot - Number of reported content type  per Company

#4
def plot_reports_per_content_type_per_company(data, company, harm):
    """Sum all numbers for each content type for a specific company and harm and plot as a table"""
    content_type_totals_per_company = {}

    if company in data and harm in data[company]:
        content_types = data[company][harm]
        for content_type, content_data in content_types.items():
            if content_type not in content_type_totals_per_company:
                content_type_totals_per_company[content_type] = 0
            for moderation_action in content_data.values():
                for count in moderation_action.values():
                    content_type_totals_per_company[content_type] += count
    else:
        print(f"No data found for company: {company} or harm: {harm}")
        return None

    data_for_df = {'Company': [], 'Content Type': [], 'N# Actions': []}
    for content_type, total_actions in content_type_totals_per_company.items():
        data_for_df['Company'].append(company)
        data_for_df['Content Type'].append(content_type)
        data_for_df['N# Actions'].append(total_actions)

    df_content_type_per_company = pd.DataFrame(data_for_df).dropna()

    content_type_descriptions = {
        '["CONTENT_TYPE_OTHER"]': 'OTHER',
        '["CONTENT_TYPE_SYNTHETIC_MEDIA"]': 'SYNTHETIC MEDIA',
        '["CONTENT_TYPE_IMAGE"]': 'IMAGE',
        '["CONTENT_TYPE_TEXT"]': 'TEXT',
        '["CONTENT_TYPE_VIDEO"]': 'VIDEO',
        '["CONTENT_TYPE_PRODUCT"]': 'PRODUCT',
        '["CONTENT_TYPE_APP"]': 'APP',
        '["CONTENT_TYPE_AUDIO"]': 'AUDIO',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT"]': 'IMAGE/TEXT',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'IMAGE/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_TEXT"],"CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO/IMAGE',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_VIDEO"]': 'AUDIO/IMAGE/VIDEO'
    }

    df_content_type_per_company['Content Type'] = df_content_type_per_company['Content Type'].map(content_type_descriptions)

    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_content_type_per_company.values, colLabels=df_content_type_per_company.columns, cellLoc='center', loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    plt.show()
    return fig



######### Data General plot - Number of reported moderation action per Company

#3

def plot_reports_per_moderation_action_per_company(data, company, harm):
    """Sum all numbers for each moderation action per company and plot as a table"""
    moderation_action_totals_per_company = {company: {} for company in data.keys()}
    for company, harms in data.items():
        if company == company:
            if harm in harms:
                for content_type in harms[harm].values():
                    for moderation_action, action_data in content_type.items():
                        if moderation_action not in moderation_action_totals_per_company[company]:
                            moderation_action_totals_per_company[company][moderation_action] = 0
                        for count in action_data.values():
                            if pd.notna(count):  # Check if the count is not NaN
                                moderation_action_totals_per_company[company][moderation_action] += count
            else:
                print(f"No data found for harm: {harm} for company: {company}")
                return None

    data_for_df = {'Company': [], 'Moderation Action': [], 'N# Actions': []}
    for company, moderation_actions in moderation_action_totals_per_company.items():
        if company == company:
            for moderation_action, total_actions in moderation_actions.items():
                data_for_df['Company'].append(company)
                data_for_df['Moderation Action'].append(moderation_action)
                data_for_df['N# Actions'].append(total_actions)

    df_moderation_action_per_company = pd.DataFrame(data_for_df).dropna()

    visibility_descriptions = {
    '["DECISION_VISIBILITY_CONTENT_REMOVED"]': 'REMOVED',
    '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED","DECISION_VISIBILITY_CONTENT_REMOVED"]': 'RESTRICTED/REMOVED',
    '["DECISION_VISIBILITY_CONTENT_REMOVED","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'REMOVED/AGE RESTRICTED',
    '["DECISION_VISIBILITY_OTHER","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'OTHER/AGE RESTRICTED',
    '["DECISION_VISIBILITY_CONTENT_LABELLED"]': 'LABELLED',
    '["DECISION_VISIBILITY_OTHER"]': 'OTHER',
    '["DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'AGE RESTRICTED',
    '["DECISION_VISIBILITY_CONTENT_DISABLED"]': 'DISABLED',
    '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED"]': 'INTERACTION RESTRICTED',
    '[]': 'NOT DEFINED',
    '["DECISION_VISIBILITY_CONTENT_DEMOTED"]': 'DEMOTED'

    }

    df_moderation_action_per_company['Moderation Action'] = df_moderation_action_per_company['Moderation Action'].map(visibility_descriptions)



    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_moderation_action_per_company.values, colLabels=df_moderation_action_per_company.columns, cellLoc='center', loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    plt.show()
    return fig


######### Data General plot - Number of reported moderation type  per Company

 #2

def generate_automation_status_report(data, company, harm):
    """ Generate automation status report for a specific company and harm """
    # Sum all numbers for each automation status per company
    automation_status_totals_per_company = {company: {}}
    harms = data.get(company, {}).get(harm, {})
    for content_type in harms.values():
        for moderation_action in content_type.values():
            for automation_status, count in moderation_action.items():
                if automation_status not in automation_status_totals_per_company[company]:
                    automation_status_totals_per_company[company][automation_status] = 0
                if pd.notna(count):  # Check if the count is not NaN
                    automation_status_totals_per_company[company][automation_status] += count

    # Prepare data for DataFrame
    data_for_df = {'Company': [], 'Harm': [], 'Automation Status': [], 'N# Actions': []}
    for automation_status, total_actions in automation_status_totals_per_company[company].items():
        data_for_df['Company'].append(company)
        data_for_df['Harm'].append(harm)  # Include the selected_harm here
        data_for_df['Automation Status'].append(automation_status)
        data_for_df['N# Actions'].append(total_actions)

    # Create DataFrame
    df_automation_status_per_company = pd.DataFrame(data_for_df).dropna()

    category_descriptions = {
        'STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE': 'PLATFORM SCOPE',
        'STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS': 'GDPR VIOLATION',
        'STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT': 'PORN/SEX CONTENT',
        'STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH': 'ILLEGAL/HARMFULL SPEECH',
        'STATEMENT_CATEGORY_VIOLENCE': 'VIOLENCE',
        'STATEMENT_CATEGORY_SCAMS_AND_FRAUD': 'SCAMS/FRAUD',
        'STATEMENT_CATEGORY_UNSAFE_AND_ILLEGAL_PRODUCTS': 'ILLEGAL PRODUCTS',
        'STATEMENT_CATEGORY_NON_CONSENSUAL_BEHAVIOUR': 'NON CONSENSUAL BEHAVIOUR',
        'STATEMENT_CATEGORY_PROTECTION_OF_MINORS': 'PROTECT MINORS',
        'STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS': 'COPYRIGHT',
        'STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS': 'NEGATIVE EFFECTS ELECTIONS',
        'STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY': 'RISK PUBLIC SECURITY',
        'STATEMENT_CATEGORY_ANIMAL_WELFARE': 'ANIMAL WELFARE',
        'STATEMENT_CATEGORY_SELF_HARM': 'SELF HARM'
    }

    automated_decision_cleaned = {
            'AUTOMATED_DECISION_FULLY': 'Fully Automated',
            'AUTOMATED_DECISION_NOT_AUTOMATED': 'Not Automated',
            'AUTOMATED_DECISION_PARTIALLY': 'Partially automated',
    }


    df_automation_status_per_company['Automation Status'] = df_automation_status_per_company['Automation Status'].map(automated_decision_cleaned)
    df_automation_status_per_company['Harm'] = df_automation_status_per_company['Harm'].map(category_descriptions)


    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_automation_status_per_company.values,
                     colLabels=df_automation_status_per_company.columns,
                     cellLoc='center',
                     loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Prepare data for stacked bar chart
    pivot_df = df_automation_status_per_company.pivot(index='Company',
                                                      columns='Automation Status',
                                                      values='N# Actions')
    pivot_df = pivot_df.fillna(0)  # Replace NaNs with 0 for plotting

    # Plotting the stacked bar chart
    pivot_df.plot(kind='bar', stacked=True, figsize=(10, 7))

    plt.title(f'Stacked Bar Chart for {company}')
    plt.xlabel('Company')
    plt.ylabel('Number of Actions')
    plt.legend(title='Automation Status', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    return fig


######### Data General plot - Number of reported content type  per Harm


def generate_harm_content_type_report(data, company, harm):
    """ Generate harm content type report for a specific company and harm """
    # Sum all numbers for each harm per content type for a specific company
    harm_content_type_totals = {}
    
    if company in data:
        company_data = data[company]
        if harm in company_data:
            harm_data = company_data[harm]
            for content_type, content_type_data in harm_data.items():
                if (harm, content_type) not in harm_content_type_totals:
                    harm_content_type_totals[(harm, content_type)] = 0
                for moderation_action in content_type_data.values():
                    for count in moderation_action.values():
                        if pd.notna(count):  # Check if the count is not NaN
                            harm_content_type_totals[(harm, content_type)] += count
    else:
        print(f"No data found for company: {company}")
    
    # Prepare data for DataFrame
    data_for_df = {'Company': [], 'Harm': [], 'Content Type': [], 'N# Actions': []}
    for (harm, content_type), total_actions in harm_content_type_totals.items():
        data_for_df['Company'].append(company)
        data_for_df['Harm'].append(harm)
        data_for_df['Content Type'].append(content_type)
        data_for_df['N# Actions'].append(total_actions)

    # Create DataFrame
    df_harm_content_type = pd.DataFrame(data_for_df).dropna()

    category_descriptions = {
        'STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE': 'PLATFORM SCOPE',
        'STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS': 'GDPR VIOLATION',
        'STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT': 'PORN/SEX CONTENT',
        'STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH': 'ILLEGAL/HARMFULL SPEECH',
        'STATEMENT_CATEGORY_VIOLENCE': 'VIOLENCE',
        'STATEMENT_CATEGORY_SCAMS_AND_FRAUD': 'SCAMS/FRAUD',
        'STATEMENT_CATEGORY_UNSAFE_AND_ILLEGAL_PRODUCTS': 'ILLEGAL PRODUCTS',
        'STATEMENT_CATEGORY_NON_CONSENSUAL_BEHAVIOUR': 'NON CONSENSUAL BEHAVIOUR',
        'STATEMENT_CATEGORY_PROTECTION_OF_MINORS': 'PROTECT MINORS',
        'STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS': 'COPYRIGHT',
        'STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS': 'NEGATIVE EFFECTS ELECTIONS',
        'STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY': 'RISK PUBLIC SECURITY',
        'STATEMENT_CATEGORY_ANIMAL_WELFARE': 'ANIMAL WELFARE',
        'STATEMENT_CATEGORY_SELF_HARM': 'SELF HARM'
    }

    content_type_descriptions = {
        '["CONTENT_TYPE_OTHER"]': 'OTHER',
        '["CONTENT_TYPE_SYNTHETIC_MEDIA"]': 'SYNTHETIC MEDIA',
        '["CONTENT_TYPE_IMAGE"]': 'IMAGE',
        '["CONTENT_TYPE_TEXT"]': 'TEXT',
        '["CONTENT_TYPE_VIDEO"]': 'VIDEO',
        '["CONTENT_TYPE_PRODUCT"]': 'PRODUCT',
        '["CONTENT_TYPE_APP"]': 'APP',
        '["CONTENT_TYPE_AUDIO"]': 'AUDIO',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT"]': 'IMAGE/TEXT',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'IMAGE/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_TEXT"],"CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO/IMAGE',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_VIDEO"]': 'AUDIO/IMAGE/VIDEO'
    }

    df_harm_content_type['Harm'] = df_harm_content_type['Harm'].map(category_descriptions)
    df_harm_content_type['Content Type'] = df_harm_content_type['Content Type'].map(content_type_descriptions)





    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_harm_content_type.values,
                     colLabels=df_harm_content_type.columns,
                     cellLoc='center',
                     loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Displaying the table
    plt.show()

    return fig



######### Data General plot - Number of reported Moderation Action  per Harm
def generate_harm_moderation_action_report(data, company, harm):
    """ Generate harm moderation action report for a specific company and harm """
    # Sum all numbers for each harm per moderation action for a specific company
    harm_moderation_action_totals = {}
    
    if company in data:
        company_data = data[company]
        if harm in company_data:
            harm_data = company_data[harm]
            for content_type, content_type_data in harm_data.items():
                for moderation_action, moderation_action_data in content_type_data.items():
                    if (harm, moderation_action) not in harm_moderation_action_totals:
                        harm_moderation_action_totals[(harm, moderation_action)] = 0
                    for count in moderation_action_data.values():
                        if pd.notna(count):  # Check if the count is not NaN
                            harm_moderation_action_totals[(harm, moderation_action)] += count
    else:
        print(f"No data found for company: {company}")
    
    # Prepare data for DataFrame
    data_for_df = {'Company': [], 'Harm': [], 'Moderation Action': [], 'N# Actions': []}
    for (harm, moderation_action), total_actions in harm_moderation_action_totals.items():
        data_for_df['Company'].append(company)
        data_for_df['Harm'].append(harm)
        data_for_df['Moderation Action'].append(moderation_action)
        data_for_df['N# Actions'].append(total_actions)

    # Create DataFrame
    df_harm_moderation_action = pd.DataFrame(data_for_df).dropna()

    category_descriptions = {
        'STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE': 'PLATFORM SCOPE',
        'STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS': 'GDPR VIOLATION',
        'STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT': 'PORN/SEX CONTENT',
        'STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH': 'ILLEGAL/HARMFULL SPEECH',
        'STATEMENT_CATEGORY_VIOLENCE': 'VIOLENCE',
        'STATEMENT_CATEGORY_SCAMS_AND_FRAUD': 'SCAMS/FRAUD',
        'STATEMENT_CATEGORY_UNSAFE_AND_ILLEGAL_PRODUCTS': 'ILLEGAL PRODUCTS',
        'STATEMENT_CATEGORY_NON_CONSENSUAL_BEHAVIOUR': 'NON CONSENSUAL BEHAVIOUR',
        'STATEMENT_CATEGORY_PROTECTION_OF_MINORS': 'PROTECT MINORS',
        'STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS': 'COPYRIGHT',
        'STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS': 'NEGATIVE EFFECTS ELECTIONS',
        'STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY': 'RISK PUBLIC SECURITY',
        'STATEMENT_CATEGORY_ANIMAL_WELFARE': 'ANIMAL WELFARE',
        'STATEMENT_CATEGORY_SELF_HARM': 'SELF HARM'
    }

    visibility_descriptions = {
    '["DECISION_VISIBILITY_CONTENT_REMOVED"]': 'REMOVED',
    '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED","DECISION_VISIBILITY_CONTENT_REMOVED"]': 'RESTRICTED/REMOVED',
    '["DECISION_VISIBILITY_CONTENT_REMOVED","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'REMOVED/AGE RESTRICTED',
    '["DECISION_VISIBILITY_OTHER","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'OTHER/AGE RESTRICTED',
    '["DECISION_VISIBILITY_CONTENT_LABELLED"]': 'LABELLED',
    '["DECISION_VISIBILITY_OTHER"]': 'OTHER',
    '["DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'AGE RESTRICTED',
    '["DECISION_VISIBILITY_CONTENT_DISABLED"]': 'DISABLED',
    '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED"]': 'INTERACTION RESTRICTED',
    '[]': 'NOT DEFINED',
    '["DECISION_VISIBILITY_CONTENT_DEMOTED"]': 'DEMOTED'

    }

    df_harm_moderation_action['Harm'] = df_harm_moderation_action['Harm'].map(category_descriptions)
    df_harm_moderation_action['Moderation Action'] = df_harm_moderation_action['Moderation Action'].map(visibility_descriptions)




    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_harm_moderation_action.values,
                     colLabels=df_harm_moderation_action.columns,
                     cellLoc='center',
                     loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Displaying the table
    plt.show()

    return fig


######### Data General plot - Number of reported Automatioin type per Harm
def generate_harm_automation_status_report(data, company, harm):
    """ Generate harm automation status report for a specific company and harm """
    # Sum all numbers for each harm per automation status for a specific company
    harm_automation_status_totals = {}
    
    if company in data:
        company_data = data[company]
        if harm in company_data:
            harm_data = company_data[harm]
            for content_type, content_type_data in harm_data.items():
                for moderation_action, moderation_action_data in content_type_data.items():
                    for automation_status, count in moderation_action_data.items():
                        if (harm, automation_status) not in harm_automation_status_totals:
                            harm_automation_status_totals[(harm, automation_status)] = 0
                        if pd.notna(count):  # Check if the count is not NaN
                            harm_automation_status_totals[(harm, automation_status)] += count
    else:
        print(f"No data found for company: {company}")
    
    # Prepare data for DataFrame
    data_for_df = {'Company': [], 'Harm': [], 'Automation Status': [], 'N# Actions': []}
    for (harm, automation_status), total_actions in harm_automation_status_totals.items():
        data_for_df['Company'].append(company)
        data_for_df['Harm'].append(harm)
        data_for_df['Automation Status'].append(automation_status)
        data_for_df['N# Actions'].append(total_actions)

    # Create DataFrame
    df_harm_automation_status = pd.DataFrame(data_for_df).dropna()

    category_descriptions = {
        'STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE': 'PLATFORM SCOPE',
        'STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS': 'GDPR VIOLATION',
        'STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT': 'PORN/SEX CONTENT',
        'STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH': 'ILLEGAL/HARMFULL SPEECH',
        'STATEMENT_CATEGORY_VIOLENCE': 'VIOLENCE',
        'STATEMENT_CATEGORY_SCAMS_AND_FRAUD': 'SCAMS/FRAUD',
        'STATEMENT_CATEGORY_UNSAFE_AND_ILLEGAL_PRODUCTS': 'ILLEGAL PRODUCTS',
        'STATEMENT_CATEGORY_NON_CONSENSUAL_BEHAVIOUR': 'NON CONSENSUAL BEHAVIOUR',
        'STATEMENT_CATEGORY_PROTECTION_OF_MINORS': 'PROTECT MINORS',
        'STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS': 'COPYRIGHT',
        'STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS': 'NEGATIVE EFFECTS ELECTIONS',
        'STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY': 'RISK PUBLIC SECURITY',
        'STATEMENT_CATEGORY_ANIMAL_WELFARE': 'ANIMAL WELFARE',
        'STATEMENT_CATEGORY_SELF_HARM': 'SELF HARM'
    }

    automated_decision_cleaned = {
            'AUTOMATED_DECISION_FULLY': 'Fully Automated',
            'AUTOMATED_DECISION_NOT_AUTOMATED': 'Not Automated',
            'AUTOMATED_DECISION_PARTIALLY': 'Partially automated',
    }


    df_harm_automation_status['Automation Status'] = df_harm_automation_status['Automation Status'].map(automated_decision_cleaned)

    df_harm_automation_status['Harm'] = df_harm_automation_status['Harm'].map(category_descriptions)

    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_harm_automation_status.values,
                     colLabels=df_harm_automation_status.columns,
                     cellLoc='center',
                     loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Displaying the table
    plt.show()

    return fig




######### Data General plot - Number of reported Moderation type  per Automation status


def generate_content_type_automation_status_report(data, company, harm):
    """ Generate content type automation status report for a specific company and harm """
    # Sum all numbers for each content type per automation status for a specific company
    content_type_automation_status_totals = {}
    
    if company in data:
        company_data = data[company]
        if harm in company_data:
            harm_data = company_data[harm]
            for content_type, content_type_data in harm_data.items():
                for moderation_action_data in content_type_data.values():
                    for automation_status, count in moderation_action_data.items():
                        if (content_type, automation_status) not in content_type_automation_status_totals:
                            content_type_automation_status_totals[(content_type, automation_status)] = 0
                        if pd.notna(count):  # Check if the count is not NaN
                            content_type_automation_status_totals[(content_type, automation_status)] += count
    else:
        print(f"No data found for company: {company}")
    
    # Prepare data for DataFrame
    data_for_df = {'Company': [], 'Content Type': [], 'Automation Status': [], 'N# Actions': []}
    for (content_type, automation_status), total_actions in content_type_automation_status_totals.items():
        data_for_df['Company'].append(company)
        data_for_df['Content Type'].append(content_type)
        data_for_df['Automation Status'].append(automation_status)
        data_for_df['N# Actions'].append(total_actions)

    # Create DataFrame
    df_content_type_automation_status = pd.DataFrame(data_for_df).dropna()


    content_type_descriptions = {
            '["CONTENT_TYPE_OTHER"]': 'OTHER',
            '["CONTENT_TYPE_SYNTHETIC_MEDIA"]': 'SYNTHETIC MEDIA',
            '["CONTENT_TYPE_IMAGE"]': 'IMAGE',
            '["CONTENT_TYPE_TEXT"]': 'TEXT',
            '["CONTENT_TYPE_VIDEO"]': 'VIDEO',
            '["CONTENT_TYPE_PRODUCT"]': 'PRODUCT',
            '["CONTENT_TYPE_APP"]': 'APP',
            '["CONTENT_TYPE_AUDIO"]': 'AUDIO',
            '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT"]': 'IMAGE/TEXT',
            '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'IMAGE/TEXT/VIDEO',
            '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_TEXT"],"CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO',
            '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO/IMAGE',
            '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_VIDEO"]': 'AUDIO/IMAGE/VIDEO'
        }
    
    automated_decision_cleaned = {
            'AUTOMATED_DECISION_FULLY': 'Fully Automated',
            'AUTOMATED_DECISION_NOT_AUTOMATED': 'Not Automated',
            'AUTOMATED_DECISION_PARTIALLY': 'Partially automated',
    }


    df_content_type_automation_status['Automation Status'] = df_content_type_automation_status['Automation Status'].map(automated_decision_cleaned)
    
    df_content_type_automation_status['Content Type'] = df_content_type_automation_status['Content Type'].map(content_type_descriptions)

        


    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_content_type_automation_status.values,
                     colLabels=df_content_type_automation_status.columns,
                     cellLoc='center',
                     loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Displaying the table
    plt.show()

    return fig




######### Data General plot - Number of reported Moderation action  per Content Type

#8

def generate_content_type_moderation_action_report(data, company, harm):
    """ Generate content type moderation action report for a specific company and harm """
    # Sum all numbers for each content type per moderation action for a specific company
    content_type_moderation_action_totals = {}
    
    if company in data:
        company_data = data[company]
        if harm in company_data:
            harm_data = company_data[harm]
            for content_type, content_type_data in harm_data.items():
                for moderation_action, moderation_action_data in content_type_data.items():
                    if (content_type, moderation_action) not in content_type_moderation_action_totals:
                        content_type_moderation_action_totals[(content_type, moderation_action)] = 0
                    for count in moderation_action_data.values():
                        if pd.notna(count):  # Check if the count is not NaN
                            content_type_moderation_action_totals[(content_type, moderation_action)] += count
    else:
        print(f"No data found for company: {company}")
    
    # Prepare data for DataFrame
    data_for_df = {'Company': [], 'Content Type': [], 'Moderation Action': [], 'N# Actions': []}
    for (content_type, moderation_action), total_actions in content_type_moderation_action_totals.items():
        data_for_df['Company'].append(company)
        data_for_df['Content Type'].append(content_type)
        data_for_df['Moderation Action'].append(moderation_action)
        data_for_df['N# Actions'].append(total_actions)

    # Create DataFrame
    df_content_type_moderation_action = pd.DataFrame(data_for_df).dropna()

    visibility_descriptions = {
    '["DECISION_VISIBILITY_CONTENT_REMOVED"]': 'REMOVED',
    '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED","DECISION_VISIBILITY_CONTENT_REMOVED"]': 'RESTRICTED/REMOVED',
    '["DECISION_VISIBILITY_CONTENT_REMOVED","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'REMOVED/AGE RESTRICTED',
    '["DECISION_VISIBILITY_OTHER","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'OTHER/AGE RESTRICTED',
    '["DECISION_VISIBILITY_CONTENT_LABELLED"]': 'LABELLED',
    '["DECISION_VISIBILITY_OTHER"]': 'OTHER',
    '["DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'AGE RESTRICTED',
    '["DECISION_VISIBILITY_CONTENT_DISABLED"]': 'DISABLED',
    '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED"]': 'INTERACTION RESTRICTED',
    '[]': 'NOT DEFINED',
    '["DECISION_VISIBILITY_CONTENT_DEMOTED"]': 'DEMOTED'

    }

    content_type_descriptions = {
        '["CONTENT_TYPE_OTHER"]': 'OTHER',
        '["CONTENT_TYPE_SYNTHETIC_MEDIA"]': 'SYNTHETIC MEDIA',
        '["CONTENT_TYPE_IMAGE"]': 'IMAGE',
        '["CONTENT_TYPE_TEXT"]': 'TEXT',
        '["CONTENT_TYPE_VIDEO"]': 'VIDEO',
        '["CONTENT_TYPE_PRODUCT"]': 'PRODUCT',
        '["CONTENT_TYPE_APP"]': 'APP',
        '["CONTENT_TYPE_AUDIO"]': 'AUDIO',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT"]': 'IMAGE/TEXT',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'IMAGE/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_TEXT"],"CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO/IMAGE',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_VIDEO"]': 'AUDIO/IMAGE/VIDEO'
    }

    # Renaming the content type categories in the DataFrame
    df_content_type_moderation_action['Moderation Action'] = df_content_type_moderation_action['Moderation Action'].map(visibility_descriptions)
    df_content_type_moderation_action['Content Type'] = df_content_type_moderation_action['Content Type'].map(content_type_descriptions)

    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_content_type_moderation_action.values,
                     colLabels=df_content_type_moderation_action.columns,
                     cellLoc='center',
                     loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Displaying the table
    plt.show()

    return fig



######### Data General plot - Number of reported Moderation type  per Moderation Action


def generate_moderation_action_automation_status_report(data, company, harm):
    """ Generate moderation action automation status report for a specific company and harm """
    # Sum all numbers for each moderation action per automation status for a specific company
    moderation_action_automation_status_totals = {}
    
    if company in data:
        company_data = data[company]
        if harm in company_data:
            harm_data = company_data[harm]
            for content_type_data in harm_data.values():
                for moderation_action, moderation_action_data in content_type_data.items():
                    for automation_status, count in moderation_action_data.items():
                        if (harm, moderation_action, automation_status) not in moderation_action_automation_status_totals:
                            moderation_action_automation_status_totals[(harm, moderation_action, automation_status)] = 0
                        if pd.notna(count):  # Check if the count is not NaN
                            moderation_action_automation_status_totals[(harm, moderation_action, automation_status)] += count
    else:
        print(f"No data found for company: {company}")
    
    # Prepare data for DataFrame
    data_for_df = {'Company': [], 'Harm': [], 'Moderation Action': [], 'Automation Status': [], 'N# Actions': []}
    for (harm, moderation_action, automation_status), total_actions in moderation_action_automation_status_totals.items():
        data_for_df['Company'].append(company)
        data_for_df['Harm'].append(harm)
        data_for_df['Moderation Action'].append(moderation_action)
        data_for_df['Automation Status'].append(automation_status)
        data_for_df['N# Actions'].append(total_actions)

        category_descriptions = {
        'STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE': 'PLATFORM SCOPE',
        'STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS': 'GDPR VIOLATION',
        'STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT': 'PORN/SEX CONTENT',
        'STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH': 'ILLEGAL/HARMFULL SPEECH',
        'STATEMENT_CATEGORY_VIOLENCE': 'VIOLENCE',
        'STATEMENT_CATEGORY_SCAMS_AND_FRAUD': 'SCAMS/FRAUD',
        'STATEMENT_CATEGORY_UNSAFE_AND_ILLEGAL_PRODUCTS': 'ILLEGAL PRODUCTS',
        'STATEMENT_CATEGORY_NON_CONSENSUAL_BEHAVIOUR': 'NON CONSENSUAL BEHAVIOUR',
        'STATEMENT_CATEGORY_PROTECTION_OF_MINORS': 'PROTECT MINORS',
        'STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS': 'COPYRIGHT',
        'STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS': 'NEGATIVE EFFECTS ELECTIONS',
        'STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY': 'RISK PUBLIC SECURITY',
        'STATEMENT_CATEGORY_ANIMAL_WELFARE': 'ANIMAL WELARE',
        'STATEMENT_CATEGORY_SELF_HARM': 'SELF HARM'

         }

        visibility_descriptions = {
        '["DECISION_VISIBILITY_CONTENT_REMOVED"]': 'REMOVED',
        '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED","DECISION_VISIBILITY_CONTENT_REMOVED"]': 'RESTRICTED/REMOVED',
        '["DECISION_VISIBILITY_CONTENT_REMOVED","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'REMOVED/AGE RESTRICTED',
        '["DECISION_VISIBILITY_OTHER","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'OTHER/AGE RESTRICTED',
        '["DECISION_VISIBILITY_CONTENT_LABELLED"]': 'LABELLED',
        '["DECISION_VISIBILITY_OTHER"]': 'OTHER',
        '["DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'AGE RESTRICTED',
        '["DECISION_VISIBILITY_CONTENT_DISABLED"]': 'DISABLED',
        '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED"]': 'INTERACTION RESTRICTED',
        '[]': 'NOT DEFINED',
        '["DECISION_VISIBILITY_CONTENT_DEMOTED"]': 'DEMOTED'

        }

        automated_decision_cleaned = {
            'AUTOMATED_DECISION_FULLY': 'Fully Automated',
            'AUTOMATED_DECISION_NOT_AUTOMATED': 'Not Automated',
            'AUTOMATED_DECISION_PARTIALLY': 'Partially automated',
    }

    
    # Create DataFrame
    df_moderation_action_automation_status = pd.DataFrame(data_for_df).dropna()

    df_moderation_action_automation_status ['Harm'] = df_moderation_action_automation_status['Harm'].map(category_descriptions)
    df_moderation_action_automation_status ['Moderation Action'] = df_moderation_action_automation_status ['Moderation Action'].map(visibility_descriptions)
    df_moderation_action_automation_status ['Automation Status'] = df_moderation_action_automation_status ['Automation Status'].map(automated_decision_cleaned)


    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_moderation_action_automation_status.values,
                     colLabels=df_moderation_action_automation_status.columns,
                     cellLoc='center',
                     loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Displaying the table
    plt.show()

    return fig





###################################################