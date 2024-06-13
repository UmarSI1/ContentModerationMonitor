import pickle
import zipfile
from pathlib import Path
from collections import defaultdict
import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st




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



######### Data General plot - Total number of Moderation Actions per Type of Content
def generate_content_type_table_and_plot(data, company):
    """ Sum all numbers for each content type across the specified company """
    content_type_totals = {}
    if company in data:  # Check if the specified company exists
        company_data = data[company]
        for harm in company_data.values():
            for content_type, content_data in harm.items():
                if content_type not in content_type_totals:
                    content_type_totals[content_type] = 0
                for moderation_action in content_data.values():
                    for automation_status in moderation_action.values():
                        content_type_totals[content_type] += automation_status

    # Create DataFrame
    content_type_data = {
        'Company': [company] * len(content_type_totals),
        'Content Type': list(content_type_totals.keys()),
        'N# Actions': list(content_type_totals.values())
    }
    df_content_type = pd.DataFrame(content_type_data).dropna()

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

    df_content_type['Content Type'] = df_content_type['Content Type'].map(content_type_descriptions)



    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_content_type.values, colLabels=df_content_type.columns, cellLoc='center', loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    return fig



######### Data General plot - Total number of Moderation Actions per Type of Moderation Actions

def generate_moderation_action_table_and_plot(data, company):
    """ Sum all numbers for each moderation action for a specific company """
    moderation_action_totals = {}
    if company in data:
        company_data = data[company]
        for harm in company_data.values():
            for content_type in harm.values():
                for moderation_action, action_data in content_type.items():
                    if moderation_action not in moderation_action_totals:
                        moderation_action_totals[moderation_action] = 0
                    for automation_status in action_data.values():
                        moderation_action_totals[moderation_action] += automation_status

    # Create DataFrame
    moderation_action_data = {
        'Company': [company] * len(moderation_action_totals),
        'Moderation Action': list(moderation_action_totals.keys()),
        'N# Actions': list(moderation_action_totals.values())
    }
    df_moderation_action = pd.DataFrame(moderation_action_data).dropna()

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

    return fig


######### Data General plot - Total number of Moderation Actions per Type of Moderation

def generate_automation_status_table_and_plot(data, company):
    """ Sum all numbers for each automation status for a specific company """
    automation_status_totals = {}
    if company in data:
        company_data = data[company]
        for harm in company_data.values():
            for content_type in harm.values():
                for moderation_action in content_type.values():
                    for automation_status, count in moderation_action.items():
                        if automation_status not in automation_status_totals:
                            automation_status_totals[automation_status] = 0
                        automation_status_totals[automation_status] += count

    # Create DataFrame
    automation_status_data = {
        'Company': [company] * len(automation_status_totals),
        'Automation Status': list(automation_status_totals.keys()),
        'N# Actions': list(automation_status_totals.values())
    }
    df_automation_status = pd.DataFrame(automation_status_data).dropna()


    automated_decision_cleaned = {
            'AUTOMATED_DECISION_FULLY': 'Fully Automated',
            'AUTOMATED_DECISION_NOT_AUTOMATED': 'Not Automated',
            'AUTOMATED_DECISION_PARTIALLY': 'Partially automated',
    }


    df_automation_status['Automation Status'] = df_automation_status['Automation Status'].map(automated_decision_cleaned)

    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_automation_status.values, colLabels=df_automation_status.columns, cellLoc='center', loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    return fig
# plt.show()


######### Data General plot - Number of reported Harms per Company IMPORTANT

#7
def generate_reports_per_harm_table_and_plot(data, company):
    """ Sum all numbers for each harm for a specific company """
    harm_totals_per_company = {}
    if company in data:
        harms = data[company]
        for harm, harm_data in harms.items():
            if harm not in harm_totals_per_company:
                harm_totals_per_company[harm] = 0
            for content_type in harm_data.values():
                for moderation_action in content_type.values():
                    for count in moderation_action.values():
                        harm_totals_per_company[harm] += count

    # Create DataFrame
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

    return fig




######### Data General plot - Number of reported content type  per Company

#4

def generate_reports_per_content_type_per_company_table_and_plot(data, specific_company):
    """ Sum all numbers for each content type per company """
    content_type_totals_per_company = {company: {} for company in data.keys()}
    for company, harms in data.items():
        for harm in harms.values():
            for content_type, content_data in harm.items():
                if content_type not in content_type_totals_per_company[company]:
                    content_type_totals_per_company[company][content_type] = 0
                for moderation_action in content_data.values():
                    for count in moderation_action.values():
                        content_type_totals_per_company[company][content_type] += count

    # Create DataFrame
    data_for_df = {'Company': [], 'Content Type': [], 'N# Actions': []}
    for company, content_types in content_type_totals_per_company.items():
        if company == specific_company:
            for content_type, total_actions in content_types.items():
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

    return fig



######### Data General plot - Number of reported moderation action per Company

#3

def generate_reports_per_moderation_action_per_company_table_and_plot(data, specific_company):
    """ Sum all numbers for each moderation action per company """
    moderation_action_totals_per_company = {company: {} for company in data.keys()}
    for company, harms in data.items():
        for harm in harms.values():
            for content_type in harm.values():
                for moderation_action, action_data in content_type.items():
                    if moderation_action not in moderation_action_totals_per_company[company]:
                        moderation_action_totals_per_company[company][moderation_action] = 0
                    for count in action_data.values():
                        if pd.notna(count):  # Check if the count is not NaN
                            moderation_action_totals_per_company[company][moderation_action] += count

    # Create DataFrame
    data_for_df = {'Company': [], 'Moderation Action': [], 'N# Actions': []}
    for company, moderation_actions in moderation_action_totals_per_company.items():
        if company == specific_company:
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

    return fig


######### Data General plot - Number of reported moderation type  per Company

 #2


def generate_reports_per_automation_status_per_company_table(data, specific_company):
    """ Sum all numbers for each automation status per company and generate a table """
    automation_status_totals_per_company = {company: {} for company in data.keys()}
    for company, harms in data.items():
        for harm in harms.values():
            for content_type in harm.values():
                for moderation_action in content_type.values():
                    for automation_status, count in moderation_action.items():
                        if automation_status not in automation_status_totals_per_company[company]:
                            automation_status_totals_per_company[company][automation_status] = 0
                        if pd.notna(count):  # Check if the count is not NaN
                            automation_status_totals_per_company[company][automation_status] += count

    data_for_df = {'Company': [], 'Automation Status': [], 'N# Actions': []}
    for company, automation_statuses in automation_status_totals_per_company.items():
        if company == specific_company:
            for automation_status, total_actions in automation_statuses.items():
                data_for_df['Company'].append(company)
                data_for_df['Automation Status'].append(automation_status)
                data_for_df['N# Actions'].append(total_actions)

    df_automation_status_per_company = pd.DataFrame(data_for_df).dropna()


    automated_decision_cleaned = {
            'AUTOMATED_DECISION_FULLY': 'Fully Automated',
            'AUTOMATED_DECISION_NOT_AUTOMATED': 'Not Automated',
            'AUTOMATED_DECISION_PARTIALLY': 'Partially automated',
    }


    df_automation_status_per_company['Automation Status'] = df_automation_status_per_company['Automation Status'].map(automated_decision_cleaned)



    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_automation_status_per_company.values, colLabels=df_automation_status_per_company.columns, cellLoc='center', loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    return fig


def generate_stacked_bar_chart_for_automation_status(data, specific_company):
    """ Generate a stacked bar chart for each automation status per company """
    automation_status_totals_per_company = {company: {} for company in data.keys()}
    for company, harms in data.items():
        for harm in harms.values():
            for content_type in harm.values():
                for moderation_action in content_type.values():
                    for automation_status, count in moderation_action.items():
                        if automation_status not in automation_status_totals_per_company[company]:
                            automation_status_totals_per_company[company][automation_status] = 0
                        if pd.notna(count):  # Check if the count is not NaN
                            automation_status_totals_per_company[company][automation_status] += count

    data_for_df = {'Company': [], 'Automation Status': [], 'N# Actions': []}
    for company, automation_statuses in automation_status_totals_per_company.items():
        if company == specific_company:
            for automation_status, total_actions in automation_statuses.items():
                data_for_df['Company'].append(company)
                data_for_df['Automation Status'].append(automation_status)
                data_for_df['N# Actions'].append(total_actions)

    df_automation_status_per_company = pd.DataFrame(data_for_df).dropna()

    automated_decision_cleaned = {
            'AUTOMATED_DECISION_FULLY': 'Fully Automated',
            'AUTOMATED_DECISION_NOT_AUTOMATED': 'Not Automated',
            'AUTOMATED_DECISION_PARTIALLY': 'Partially automated',
    }


    df_automation_status_per_company['Automation Status'] = df_automation_status_per_company['Automation Status'].map(automated_decision_cleaned)



    # Prepare data for stacked bar chart
    pivot_df = df_automation_status_per_company.pivot(index='Company', columns='Automation Status', values='N# Actions')
    pivot_df = pivot_df.fillna(0)  # Replace NaNs with 0 for plotting

    # Plotting the stacked bar chart
    fig, ax = plt.subplots(figsize=(10, 7))
    pivot_df.plot(kind='bar', stacked=True, ax=ax)

    plt.title(f'Stacked Bar Chart for {specific_company}')
    plt.xlabel('Company')
    plt.ylabel('Number of Actions')
    plt.legend(title='Automation Status', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    return fig



######### Data General plot - Number of reported content type  per Harm

def generate_reports_per_harm_per_content_type_table(data, company):
    """ Sum all numbers for each harm per content type for a specific company and generate a table """
    harm_content_type_totals = {}
    if company in data:
        company_data = data[company]
        for harm, harm_data in company_data.items():
            for content_type, content_type_data in harm_data.items():
                if (harm, content_type) not in harm_content_type_totals:
                    harm_content_type_totals[(harm, content_type)] = 0
                for moderation_action in content_type_data.values():
                    for count in moderation_action.values():
                        if pd.notna(count):  # Check if the count is not NaN
                            harm_content_type_totals[(harm, content_type)] += count

    data_for_df = {'Company': [], 'Harm': [], 'Content Type': [], 'N# Actions': []}
    for (harm, content_type), total_actions in harm_content_type_totals.items():
        data_for_df['Company'].append(company)
        data_for_df['Harm'].append(harm)
        data_for_df['Content Type'].append(content_type)
        data_for_df['N# Actions'].append(total_actions)

    df_harm_content_type = pd.DataFrame(data_for_df).dropna()

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


    df_harm_content_type['Harm'] = df_harm_content_type['Harm'].map(category_descriptions)
    df_harm_content_type['Content Type'] = df_harm_content_type['Content Type'].map(content_type_descriptions)

    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_harm_content_type.values, colLabels=df_harm_content_type.columns, cellLoc='center', loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)


######### Data General plot - Number of reported Moderation Action  per Harm
def generate_reports_per_harm_per_moderation_action_table(data, company):
    """ Sum all numbers for each harm per moderation action for a specific company and generate a table """
    harm_moderation_action_totals = {}
    if company in data:
        company_data = data[company]
        for harm, harm_data in company_data.items():
            for content_type, content_type_data in harm_data.items():
                for moderation_action, moderation_action_data in content_type_data.items():
                    if (harm, moderation_action) not in harm_moderation_action_totals:
                        harm_moderation_action_totals[(harm, moderation_action)] = 0
                    for count in moderation_action_data.values():
                        if pd.notna(count):  # Check if the count is not NaN
                            harm_moderation_action_totals[(harm, moderation_action)] += count

    data_for_df = {'Company': [], 'Harm': [], 'Moderation Action': [], 'N# Actions': []}
    for (harm, moderation_action), total_actions in harm_moderation_action_totals.items():
        data_for_df['Company'].append(company)
        data_for_df['Harm'].append(harm)
        data_for_df['Moderation Action'].append(moderation_action)
        data_for_df['N# Actions'].append(total_actions)

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
    table = ax.table(cellText=df_harm_moderation_action.values, colLabels=df_harm_moderation_action.columns, cellLoc='center', loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    return fig


######### Data General plot - Number of reported Moderation type  per Harm
def generate_reports_per_harm_per_automation_status_table(data, company):
    """ Sum all numbers for each harm per automation status for a specific company and generate a table """
    harm_automation_status_totals = {}
    if company in data:
        company_data = data[company]
        for harm, harm_data in company_data.items():
            for content_type, content_type_data in harm_data.items():
                for moderation_action, moderation_action_data in content_type_data.items():
                    for automation_status, count in moderation_action_data.items():
                        if (harm, automation_status) not in harm_automation_status_totals:
                            harm_automation_status_totals[(harm, automation_status)] = 0
                        if pd.notna(count):  # Check if the count is not NaN
                            harm_automation_status_totals[(harm, automation_status)] += count

    data_for_df = {'Company': [], 'Harm': [], 'Automation Status': [], 'N# Actions': []}
    for (harm, automation_status), total_actions in harm_automation_status_totals.items():
        data_for_df['Company'].append(company)
        data_for_df['Harm'].append(harm)
        data_for_df['Automation Status'].append(automation_status)
        data_for_df['N# Actions'].append(total_actions)

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

    df_harm_automation_status['Harm'] = df_harm_automation_status['Harm'].map(category_descriptions)
    df_harm_automation_status['Automation Status'] = df_harm_automation_status['Automation Status'].map(automated_decision_cleaned)



    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_harm_automation_status.values, colLabels=df_harm_automation_status.columns, cellLoc='center', loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    return fig


######### Data General plot - Number of reported Moderation type  per Content Type

def generate_reports_per_content_type_per_automation_status_table(data, company):
    """ Sum all numbers for each content type per automation status for a specific company and generate a table """
    content_type_automation_status_totals = {}
    if company in data:
        company_data = data[company]
        for harm_data in company_data.values():
            for content_type, content_type_data in harm_data.items():
                for moderation_action_data in content_type_data.values():
                    for automation_status, count in moderation_action_data.items():
                        if (content_type, automation_status) not in content_type_automation_status_totals:
                            content_type_automation_status_totals[(content_type, automation_status)] = 0
                        if pd.notna(count):  # Check if the count is not NaN
                            content_type_automation_status_totals[(content_type, automation_status)] += count

    data_for_df = {'Company': [], 'Content Type': [], 'Automation Status': [], 'N# Actions': []}
    for (content_type, automation_status), total_actions in content_type_automation_status_totals.items():
        data_for_df['Company'].append(company)
        data_for_df['Content Type'].append(content_type)
        data_for_df['Automation Status'].append(automation_status)
        data_for_df['N# Actions'].append(total_actions)

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
    table = ax.table(cellText=df_content_type_automation_status.values, colLabels=df_content_type_automation_status.columns, cellLoc='center', loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    return fig



######### Data General plot - Number of reported Moderation action  per Content Type

#8

def generate_reports_per_content_type_per_moderation_action_table(data, company):
    """ Sum all numbers for each content type per moderation action for a specific company and generate a table """
    content_type_moderation_action_totals = {}
    if company in data:
        company_data = data[company]
        for harm_data in company_data.values():
            for content_type, content_type_data in harm_data.items():
                for moderation_action, moderation_action_data in content_type_data.items():
                    if (content_type, moderation_action) not in content_type_moderation_action_totals:
                        content_type_moderation_action_totals[(content_type, moderation_action)] = 0
                    for count in moderation_action_data.values():
                        if pd.notna(count):  # Check if the count is not NaN
                            content_type_moderation_action_totals[(content_type, moderation_action)] += count

    data_for_df = {'Company': [], 'Content Type': [], 'Moderation Action': [], 'N# Actions': []}
    for (content_type, moderation_action), total_actions in content_type_moderation_action_totals.items():
        data_for_df['Company'].append(company)
        data_for_df['Content Type'].append(content_type)
        data_for_df['Moderation Action'].append(moderation_action)
        data_for_df['N# Actions'].append(total_actions)

    df_content_type_moderation_action = pd.DataFrame(data_for_df).dropna()


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

    df_content_type_moderation_action['Content Type'] = df_content_type_moderation_action['Content Type'].map(content_type_descriptions)
    df_content_type_moderation_action['Moderation Action'] = df_content_type_moderation_action['Moderation Action'].map(visibility_descriptions)

    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_content_type_moderation_action.values, colLabels=df_content_type_moderation_action.columns, cellLoc='center', loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    return fig



######### Data General plot - Number of reported Moderation type  per Moderation Action

def generate_reports_per_moderation_action_per_automation_status_table(data, company):
    """ Sum all numbers for each moderation action per automation status for a specific company and generate a table """
    moderation_action_automation_status_totals = {}
    if company in data:
        company_data = data[company]
        for harm_data in company_data.values():
            for content_type_data in harm_data.values():
                for moderation_action, moderation_action_data in content_type_data.items():
                    for automation_status, count in moderation_action_data.items():
                        if (moderation_action, automation_status) not in moderation_action_automation_status_totals:
                            moderation_action_automation_status_totals[(moderation_action, automation_status)] = 0
                        if pd.notna(count):  # Check if the count is not NaN
                            moderation_action_automation_status_totals[(moderation_action, automation_status)] += count

    data_for_df = {'Company': [], 'Moderation Action': [], 'Automation Status': [], 'N# Actions': []}
    for (moderation_action, automation_status), total_actions in moderation_action_automation_status_totals.items():
        data_for_df['Company'].append(company)
        data_for_df['Moderation Action'].append(moderation_action)
        data_for_df['Automation Status'].append(automation_status)
        data_for_df['N# Actions'].append(total_actions)

    df_moderation_action_automation_status = pd.DataFrame(data_for_df).dropna()

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


    df_moderation_action_automation_status['Automation Status'] = df_moderation_action_automation_status['Automation Status'].map(automated_decision_cleaned)
    df_moderation_action_automation_status['Moderation Action'] = df_moderation_action_automation_status['Moderation Action'].map(visibility_descriptions)

    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_moderation_action_automation_status.values, colLabels=df_moderation_action_automation_status.columns, cellLoc='center', loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    return fig



###################################################