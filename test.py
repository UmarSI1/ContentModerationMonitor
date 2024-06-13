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





import pandas as pd
import matplotlib.pyplot as plt

def plot_reports_per_content_type_per_companyz(data, harm):
    """Sum all numbers for each content type for all companies and a specific harm and plot as a table"""
    content_type_totals_per_company = {}

    for company, company_data in data.items():
        if harm in company_data:
            content_types = company_data[harm]
            for content_type, content_data in content_types.items():
                if content_type not in content_type_totals_per_company:
                    content_type_totals_per_company[content_type] = {}
                for moderation_action in content_data.values():
                    for count in moderation_action.values():
                        if company not in content_type_totals_per_company[content_type]:
                            content_type_totals_per_company[content_type][company] = 0
                        content_type_totals_per_company[content_type][company] += count
        else:
            print(f"No data found for harm: {harm} for company: {company}")
            return None

    data_for_df = {'Company': [], 'Content Type': [], 'N# Actions': []}
    for content_type, company_data in content_type_totals_per_company.items():
        for company, total_actions in company_data.items():
            data_for_df['Company'].append(company)
            data_for_df['Content Type'].append(content_type)
            data_for_df['N# Actions'].append(total_actions)

    df_content_type_per_company = pd.DataFrame(data_for_df).dropna()

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

    # Renaming the content type categories in the DataFrame
    df_content_type_per_company['Content Type'] = df_content_type_per_company['Content Type'].map(content_type_descriptions)

    # Pivot the dataframe
    pivot_df = df_content_type_per_company.pivot_table(index='Company', columns='Content Type', values='N# Actions', fill_value=0)

    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=pivot_df.values, rowLabels=pivot_df.index, colLabels=pivot_df.columns, cellLoc='center', loc='center')

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(7)

    plt.show()
    return fig



plot_reports_per_content_type_per_companyz(data_ACC, 'STATEMENT_CATEGORY_PROTECTION_OF_MINORS')