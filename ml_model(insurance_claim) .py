
# Import Libraries
import pandas as pd
import numpy as np
import missingno as msno

import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

from sklearn.preprocessing import OneHotEncoder, LabelEncoder

from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFECV
from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import GradientBoostingClassifier

"""### Dataset Loading"""

# Load Dataset
from google.colab import drive
drive.mount('/content/drive')

data_id="/content/drive/MyDrive/TRAIN-HEALTH INSURANCE CROSS SELL PREDICTION.csv"
data=pd.read_csv(data_id)

"""### Dataset First View"""

# Dataset First Look
data.head()

"""### Dataset Rows & Columns count"""

# number of rows and columns
num_rows, num_columns = data.shape

print("Number of rows:", num_rows)
print("Number of columns:", num_columns)

"""### Dataset Information"""

# Information about the dataset
print("Dataset Information:")
print(data.info())

"""#### Duplicate Values"""

# Dataset Duplicate Value Count
duplicate_count = data.duplicated().sum()
print("Duplicate Value Count:", duplicate_count)

"""#### Missing Values/Null Values"""

# Missing Values/Null Values Count
# Checking missing values
missing_values = data.isnull().sum().sum()

if missing_values == 0:
    print("There are no missing values in the dataset.")
else:
    print("There are missing values in the dataset.")

# Visualize missing values (even if there are none, this can still provide a visual confirmation)
print("Visualization of Missing Values (if any):")
msno.matrix(data)

"""### What did you know about your dataset?

**Data** **Integrity**:

Number of rows: 381,109

Number of columns: 12

No missing values

No duplicate rows


**Potential** **Analysis**:

This dataset could be used for various analyses such as understanding customer demographics, predicting response to marketing campaigns, identifying factors influencing insurance purchases, etc.
Further analysis could involve exploring relationships between variables, such as how age or gender correlate with response rates, or how vehicle age relates to insurance premium.
Overall, this dataset provides comprehensive information about customers and their interactions with an insurance company, offering valuable insights for targeted marketing strategies and risk assessment.

## ***2. Understanding Your Variables***
"""

# Dataset Columns
#columns list
columns_list = data.columns.tolist()

print("Columns:", columns_list)

# Dataset Describe
# Summary statistics
print("\nSummary Statistics:")
print(data.describe())

"""### Variables Description

id: An identifier for each entry.

Gender: Categorical variable indicating the gender of the individual.

Age: Numerical variable indicating the age of the individual.

Driving_License: Binary variable indicating whether the individual has a driving license (1 for yes, 0 for no).

Region_Code: Numerical variable indicating the region code.

Previously_Insured: Binary variable indicating whether the individual was previously insured (1 for yes, 0 for no).

Vehicle_Age: Categorical variable indicating the age of the vehicle.

Vehicle_Damage: Categorical variable indicating whether the vehicle has been damaged in the past. Annual_Premium: Numerical variable indicating the annual premium.

Policy_Sales_Channel: Numerical variable indicating the policy sales channel.

Vintage: Numerical variable indicating the vintage (time period) associated with the customer.

Response: Binary variable indicating the response variable.

### Check Unique Values for each variable.
"""

# Check Unique Values for each variable.
unique_values = {}
for column in data.columns:
    unique_values[column] = data[column].unique()

# Print unique values for each column
for column, values in unique_values.items():
    print(f"\nUnique values in {column}: {values}")

"""## 3. ***Data Wrangling***

### Data Wrangling Code
"""

# Write your code to make your dataset analysis ready.
df=data.copy()

# Check data types of columns
data_types = df.dtypes
print("\nData types:")
print(data_types)

# Convert 'Region_Code' column to integer type
df['Region_Code'] = df['Region_Code'].astype(int)

# Convert 'Policy_Sales_Channel' column to integer type
df['Policy_Sales_Channel'] = df['Policy_Sales_Channel'].astype(int)

# Check the distribution of 'Age'
age_distribution = df['Age'].value_counts().sort_index()
print("\nAge Distribution:")
print(age_distribution)

# Check the distribution of categorical variables
gender_distribution = df['Gender'].value_counts()
vehicle_age_distribution = df['Vehicle_Age'].value_counts()
vehicle_damage_distribution = df['Vehicle_Damage'].value_counts()

print("\nGender Distribution:")
print(gender_distribution)

print("\nVehicle Age Distribution:")
print(vehicle_age_distribution)

print("\nVehicle Damage Distribution:")
print(vehicle_damage_distribution)

# Explore the response variable
response_distribution = df['Response'].value_counts(normalize=True)
print("\nResponse Distribution:")
print(response_distribution)

#  distribution of 'Region_Code'
region_distribution = df['Region_Code'].value_counts()
print("\nRegion Code Distribution:")
print(region_distribution)

# distribution of 'Policy_Sales_Channel'
channel_distribution = df['Policy_Sales_Channel'].value_counts()
print("\nPolicy Sales Channel Distribution:")
print(channel_distribution)

#  distribution of 'Vintage'
vintage_distribution = df['Vintage'].value_counts()
print("\nVintage Distribution:")
print(vintage_distribution)

#  distribution of 'Driving_License'
driving_license_distribution = df['Driving_License'].value_counts(normalize=True)
print("\nDriving License Distribution:")
print(driving_license_distribution)

#the average response rate for different age groups
response_by_age = df.groupby(pd.cut(df['Age'], bins=range(20, 90, 10)))['Response'].mean()
print("\nAverage Response Rate by Age Group:")
print(response_by_age)

# the average response rate for different regions
response_by_region = df.groupby('Region_Code')['Response'].mean()
print("\nAverage Response Rate by Region:")
print(response_by_region)

#  distribution of 'Previously_Insured'
previously_insured_distribution = df['Previously_Insured'].value_counts(normalize=True)
print("\nPreviously Insured Distribution:")
print(previously_insured_distribution)

#  the average annual premium for individuals with and without prior insurance
avg_premium_by_insurance = df.groupby('Previously_Insured')['Annual_Premium'].mean()
print("\nAverage Annual Premium by Previous Insurance Status:")
print(avg_premium_by_insurance)

# the average response rate for individuals with and without prior insurance
response_by_insurance = df.groupby('Previously_Insured')['Response'].mean()
print("\nAverage Response Rate by Previous Insurance Status:")
print(response_by_insurance)

#  distribution of 'Response' within different age groups
response_distribution_by_age = df.groupby(pd.cut(df['Age'], bins=range(20, 90, 10)))['Response'].value_counts(normalize=True)
print("\nResponse Distribution by Age Group:")
print(response_distribution_by_age)

#  distribution of 'Response' within different regions
response_distribution_by_region = df.groupby('Region_Code')['Response'].value_counts(normalize=True)
print("\nResponse Distribution by Region:")
print(response_distribution_by_region)

"""### What all manipulations have you done and insights you found?

**Gender Distribution:**

The dataset contains more male customers (206,089) than female customers (175,020).

**Vehicle Age Distribution:**

Majority of the vehicles fall into the '1-2 Year' category (200,316), followed by '< 1 Year' (164,786), and the least number of vehicles are '> 2 Years' (16,007).

**Vehicle Damage Distribution:**

There are slightly more vehicles with previous damage ('Yes': 192,413) compared to those without damage ('No': 188,696).

**Response Distribution:**

The majority of customers (87.74%) did not respond ('Response' = 0), while a smaller proportion (12.26%) responded positively ('Response' = 1).

There is a gender imbalance in the dataset, with more male customers than female customers.
The majority of vehicles are between 1 to 2 years old, indicating a relatively young fleet.
The dataset is fairly evenly split between vehicles with and without previous damage.
The response rate is low, with only about 12.26% of customers responding positively, suggesting a potential area for improvement in marketing or customer engagement strategies.

**Region Code Distribution:**

The dataset covers various regions, with region code 28 having the highest frequency of 106,415 occurrences, followed by 8, 46, and 41.
Some regions have very few occurrences, such as region code 42 with only 591 occurrences.

**Policy Sales Channel Distribution:**

Policy sales channel 152 appears to be the most common, with 134,784 occurrences.
There are 155 unique policy sales channels in the dataset.

**Vintage Distribution:**

The vintage variable represents the number of days since the customer was associated with the company.
There is variation in the vintage, with some values occurring more frequently than others.

**Driving License Distribution:**

The vast majority of individuals in the dataset have a driving license, with a distribution of 99.79% having a license and 0.21% without.

**Average Response Rate by Age Group:**

The average response rate tends to increase with age, with the highest response rate observed in the age group 30-40 and 40-50.

**Average Response Rate by Region:**

The response rates vary across different regions, ranging from 4.08% to 18.72%.
Some regions have notably higher or lower response rates compared to others.

**Previously Insured Distribution:**

Approximately 54.18% of individuals in the dataset are not previously insured, while 45.82% are previously insured.

**Average Annual Premium by Previous Insurance Status:**

The average annual premium for individuals without prior insurance is approximately 30,496.82 units, whereas for those with prior insurance, it is approximately 30,644.29 units. The difference in average premiums between the two groups is relatively small.

**Average Response Rate by Previous Insurance Status:**

The response rate for individuals without prior insurance is substantially higher (around 22.55%) compared to those with prior insurance (around 0.09%). This suggests that individuals without prior insurance are more likely to respond positively to insurance offers or marketing campaigns.

**Response Distribution by Age Group:**

Response rates vary across age groups. Notably, younger age groups (20-30) have a lower response rate, while older age groups tend to have higher response rates. This indicates that older individuals may be more receptive to insurance offers.

**Response Distribution by Region:**

Response rates also vary across different regions. Some regions have a higher proportion of positive responses compared to others, suggesting potential regional differences in customer behavior or response to marketing efforts.

The dataset comprises insurance-related information with 381,109 entries and 12 columns. Gender distribution indicates a slight majority of male customers. Vehicle age distribution highlights the prevalence of vehicles aged 1-2 years. Approximately 54.18% of individuals are not previously insured. The average annual premium is comparable between those previously insured and those not. However, response rates vary significantly between the two groups, with uninsured individuals showing a much higher response rate (22.55%) compared to insured individuals (0.09%). Response rates also vary across age groups and regions, with older age groups and certain regions demonstrating higher response rates. These insights suggest potential strategies for targeted marketing campaigns, emphasizing demographic factors and regional variations to optimize response rates and enhance customer engagement. Additionally, the dataset exhibits a skewed response distribution, with the majority (87.74%) not responding, highlighting an area for potential improvement in marketing effectiveness and customer outreach strategies.

## ***4. Data Vizualization, Storytelling & Experimenting with charts : Understand the relationships between variables***

#### Chart - 1-Univariate Histogram of Age:
"""

# Chart - 1 visualization code
plt.figure(figsize=(10, 6))
plt.hist(df['Age'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribution of Age')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

"""##### 1. Why did you pick the specific chart?

The specific chart chosen, a histogram, was likely selected because it's effective for displaying the distribution of data across different age groups in this case. Histograms are particularly useful for illustrating frequency distributions and identifying patterns or trends within the data.

##### 2. What is/are the insight(s) found from the chart?

The insight derived from the histogram is that there is a high frequency of individuals in the age groups of 20-30 and those nearing their 50s. This suggests that there may be distinct segments within the population that have a higher demand or need for insurance products and services.

##### 3. Will the gained insights help creating a positive business impact?
Are there any insights that lead to negative growth? Justify with specific reason.

The gained insights can potentially lead to positive business impacts. By identifying the age groups with higher frequencies, insurance companies can tailor their marketing strategies and product offerings to better target these demographics. For instance, they can develop specific insurance plans or promotional campaigns tailored to the needs and preferences of individuals in their 20s and 30s or those approaching their 50s, potentially leading to increased sales and customer satisfaction.

#### Chart - 2-Univariate Bar Plot of Gender Distribution:
"""

# Chart - 2 visualization code
plt.figure(figsize=(8, 5))
df['Gender'].value_counts().plot(kind='bar', color=['skyblue', 'salmon'])
plt.title('Gender Distribution')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.show()

"""##### 1. Why did you pick the specific chart?

A bar plot is suitable for visualizing the distribution of categorical data, such as gender. It presents a clear comparison between different categories, making it easy to identify dominant groups.

##### 2. What is/are the insight(s) found from the chart?

The insight gained from the bar plot is that the male gender dominates the distribution. This suggests that there may be a higher proportion of males compared to females within the dataset or population being analyzed.

##### 3. Will the gained insights help creating a positive business impact?
Are there any insights that lead to negative growth? Justify with specific reason.

The insight of male dominance in gender distribution can indeed help in shaping business strategies for insurance products and services. For instance, insurance companies can tailor their marketing efforts to appeal more directly to male audiences or develop specific products that cater to their needs and preferences. This targeted approach can potentially lead to increased engagement and sales among male customers.

#### Chart - 3-Bivariate Box Plot of Annual Premium by Vehicle Age:
"""

# Chart - 3 visualization code
plt.figure(figsize=(10, 6))
sns.boxplot(x='Vehicle_Age', y='Annual_Premium', data=df, palette='Set2')
plt.title('Annual Premium by Vehicle Age')
plt.xlabel('Vehicle Age')
plt.ylabel('Annual Premium')
plt.show()

"""##### 1. Why did you pick the specific chart?

A bivariate box plot is an effective visualization tool for comparing the distribution of one variable (Annual Premium) across different categories of another variable (Vehicle Age). It provides insights into the relationship between these two variables and helps identify patterns or trends.

##### 2. What is/are the insight(s) found from the chart?

The insights gained from the bivariate box plot are as follows:

For vehicles aged over 2 years: The box size is relatively large, indicating a wide range of annual premiums. However, there is a dense scatter of points around the 1 lakh mark for annual premium, suggesting that a significant number of vehicles in this age category have premiums around this value.

For vehicles aged 1-2 years: The box size is moderate, indicating a slightly narrower range of annual premiums compared to older vehicles. The scatter points tend to cluster around the 45 lakh mark for annual premium, indicating that a considerable number of vehicles in this age category have premiums around this value.

For vehicles aged less than 1 year: The box size is small, indicating a relatively narrow range of annual premiums. The scatter points tend to cluster around the 30 lakh mark for annual premium, suggesting that a significant number of newer vehicles have premiums around this value.

##### 3. Will the gained insights help creating a positive business impact?
Are there any insights that lead to negative growth? Justify with specific reason.

These insights can potentially lead to positive business impacts by helping insurance companies tailor their pricing strategies and product offerings based on vehicle age. For example, they may offer specialized insurance packages or discounts for newer vehicles with lower premiums or adjust pricing for older vehicles with higher premiums to remain competitive in the market.

However, there might also be potential negative implications. For instance, if the scatter points indicate a concentration of premiums around higher values for newer vehicles, it could suggest that insurance for newer vehicles is perceived as more costly, potentially deterring customers from purchasing insurance for newer vehicles. Therefore, insurance companies may need to carefully consider how they communicate and price insurance policies for different vehicle age categories to avoid potential negative impacts on customer acquisition and retention.

#### Chart - 4-Bivariate box Plot of Region_Code vs.Annual_Premium by Response:
"""

# Chart - 4 visualization code
plt.figure(figsize=(18, 10))
sns.boxplot(x='Region_Code', y='Annual_Premium', hue='Response', data=df, palette='coolwarm')
plt.title('Region Code vs. Annual Premium Colored by Response')
plt.xlabel('Region Code')
plt.ylabel('Annual Premium')
plt.show()

"""##### 1. Why did you pick the specific chart?

A bivariate box plot is an effective visualization for comparing the distribution of a continuous variable across different levels of a categorical variable. It allows for the assessment of central tendency, variability, and potential outliers within each category.

##### 2. What is/are the insight(s) found from the chart?

For region codes 8, 28, and 41: The box size is small, indicating a relatively narrow range of annual premiums. Additionally, there are numerous scatter points outside the whiskers of the box plots, indicating outliers. This suggests that for these region codes, there is a wide variation in annual premiums, with many instances of unusually high or low premiums. These outliers could potentially represent unique characteristics or anomalies in insurance pricing or customer behavior within these regions.

For region codes 7, 18, 36, 38, 39, and 51: The box size is large, indicating a wider range of annual premiums compared to the regions mentioned earlier. However, the maximum value of annual premiums within these regions tends to be lower, as indicated by the lower whisker of the box plot. Additionally, the majority of scatter points are concentrated around the median or quartiles of the box plots, particularly for response values of 0 and 1. This suggests that within these regions, there is a more consistent distribution of annual premiums, with fewer outliers compared to regions 8, 28, and 41.

##### 3. Will the gained insights help creating a positive business impact?
Are there any insights that lead to negative growth? Justify with specific reason.

These insights can help insurance companies understand the variability in annual premiums across different regions and how it relates to customer responses. For instance, regions with a higher frequency of outliers may require further investigation to understand the factors contributing to the wide variation in premiums. On the other hand, regions with more consistent premium distributions may present opportunities for targeted marketing or pricing strategies to attract and retain customers. However, the presence of outliers in certain regions could also indicate potential challenges, such as regulatory or economic factors affecting insurance pricing or customer behavior, which may need to be addressed to ensure business sustainability and customer satisfaction.

#### Chart - 5-Univariate Bar Plot of Previously Insured Distribution:
"""

plt.figure(figsize=(8, 5))
df['Previously_Insured'].value_counts().plot(kind='bar', color=['skyblue', 'salmon'])
plt.title('Previously Insured Distribution')
plt.xlabel('Previously Insured')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.show()

"""##### 1. Why did you pick the specific chart?

A univariate bar plot is a suitable visualization for displaying the distribution of a single categorical variable, in this case, the previously insured status of vehicles.

##### 2. What is/are the insight(s) found from the chart?

The insight gained from the univariate bar plot is that non-insured vehicles dominate the distribution. This suggests that a significant proportion of vehicles in the dataset or population being analyzed do not have insurance coverage.

##### 3. Will the gained insights help creating a positive business impact?
Are there any insights that lead to negative growth? Justify with specific reason.

Targeted marketing: Insurance companies can use this insight to tailor their marketing efforts towards individuals who do not currently have insurance coverage. They can highlight the importance of insurance and the benefits of being insured to attract these customers.
Product development: Insights from the distribution of previously insured vehicles can inform the development of new insurance products or the modification of existing ones. For example, insurers may introduce special offers or incentives to encourage non-insured vehicle owners to purchase insurance policies.
Risk assessment: Insurance companies can use this information to assess the level of risk associated with insuring non-insured vehicles. They can adjust their pricing strategies and underwriting criteria accordingly to mitigate potential risks and ensure profitability.

#### Chart - 6-Multivariate Stacked Bar Plot of Response by Previously Insured and Gender:


---
"""

# Chart - 6 visualization code
response_prev_insured_gender = df.groupby(['Previously_Insured', 'Gender'])['Response'].mean().unstack()
response_prev_insured_gender.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis')
plt.title('Response by Previously Insured and Gender')
plt.xlabel('Previously Insured')
plt.ylabel('Response Rate')
plt.xticks(ticks=[0, 1], labels=['No', 'Yes'], rotation=0)
plt.legend(title='Gender')
plt.show()

"""##### 1. Why did you pick the specific chart?

A multivariate stacked bar plot is a visual representation that allows for the comparison of multiple categorical variables simultaneously. In this case, the variables are "Response," "Previously Insured," and "Gender."

##### 2. What is/are the insight(s) found from the chart?

The insight gained from this plot is that there are no "Yes" responses among customers, indicating that none of the customers responded affirmatively to whatever prompt or question was asked. Additionally, the plot shows the distribution of responses across different categories of "Previously Insured" and "Gender."

The absence of "Yes" responses suggests that there may be issues with the prompt or question posed to customers, or it could indicate a lack of interest or engagement with the topic among the surveyed population.

##### 3. Will the gained insights help creating a positive business impact?
Are there any insights that lead to negative growth? Justify with specific reason.

While the absence of "Yes" responses does not necessarily indicate negative growth on its own, it does raise questions about the effectiveness of the survey or the appeal of the topic to the target audience. It may prompt businesses to revisit their survey methods, the clarity of their questions, or the relevance of the topic to their customers' interests and needs.

Additionally, the insights from this plot could lead to adjustments in marketing strategies, product offerings, or customer engagement initiatives to better align with customer preferences and improve response rates in future surveys or interactions. For instance, businesses may need to reevaluate their messaging or value propositions to ensure they resonate with their target audience and elicit more positive responses.

#### Chart - 7-Multivariate Facet Grid of Response by Vehicle Age and Previously Insured:


---
"""

# Chart - 7 visualization code
g = sns.FacetGrid(df, col='Previously_Insured', height=4)
g.map_dataframe(sns.histplot, x='Vehicle_Age', hue='Response', multiple='stack')
g.set_titles(col_template='Previously Insured: {col_name}')
plt.legend(title='Response')
plt.show()

"""##### 1. Why did you pick the specific chart?

A multivariate facet grid is a grid of small multiples, where each subplot represents a subset of the data based on different levels of categorical variables. In this case, the variables are "Response," "Vehicle Age," and "Previously Insured."

##### 2. What is/are the insight(s) found from the chart?

Where the data is divided into columns based on the unique values of the 'Previously_Insured' variable. Within each column, a histogram of the 'Vehicle_Age' variable is plotted, with bars stacked according to the 'Response' variable.

The first visual, focusing on "Previously Insured: 0," likely represents customers who were not previously insured. It shows the distribution of responses across different categories of "Vehicle Age" for this subset of customers.

The second visual, focusing on "Previously Insured: 1," likely represents customers who were previously insured. Similarly, it shows the distribution of responses across different categories of "Vehicle Age" for this subset of customers.

Insights from these visuals could provide valuable information about how the response to a certain prompt or question varies based on both vehicle age and previous insurance status. For example, it may reveal whether there are differences in response patterns between customers who were previously insured and those who were not, and how these patterns vary across different age groups of vehicles.

##### 3. Will the gained insights help creating a positive business impact?
Are there any insights that lead to negative growth? Justify with specific reason.

Analyzing these visuals can help businesses tailor their marketing strategies, product offerings, or customer engagement initiatives based on the characteristics of different customer segments. For instance, if there are notable differences in response patterns between previously insured and non-insured customers, businesses may need to develop targeted approaches to address the specific needs and preferences of each group.

#### Chart - 8-Bar Plot of Mean Response rate for each category of 'Vehicle_Age':
"""

# Chart - 8 visualization code
# Calculate mean response rate by vehicle age group
vehicle_age_response_mean = df.groupby('Vehicle_Age')['Response'].mean().reset_index()

# Plotting
plt.figure(figsize=(10, 6))
sns.barplot(x='Vehicle_Age', y='Response', data=vehicle_age_response_mean, palette='viridis')
plt.title('Mean Response Rate by Vehicle Age')
plt.xlabel('Vehicle Age')
plt.ylabel('Mean Response Rate')
plt.xticks(rotation=45)
plt.show()

"""##### 1. Why did you pick the specific chart?

A bar plot of the mean response rate for each category of 'Vehicle_Age' provides valuable insights into how the response variable varies across different age groups of vehicles.

##### 2. What is/are the insight(s) found from the chart?

The higher mean response rate for vehicles older than 2 years suggests that owners of older vehicles may be more responsive to insurance-related offers or messages. Insurance companies can leverage this insight to develop targeted marketing campaigns specifically tailored to owners of older vehicles. These campaigns can highlight the benefits of insurance coverage for older vehicles, such as protection against wear and tear or increased likelihood of accidents.The higher mean response rate for older vehicles may also have implications for risk assessment and pricing strategies. Insurance companies may need to adjust their underwriting criteria or premium rates to account for the increased likelihood of claims associated with older vehicles. By accurately assessing the risk associated with different age groups of vehicles, insurers can ensure that their pricing reflects the level of risk exposure, thereby maintaining profitability while remaining competitive in the market.

##### 3. Will the gained insights help creating a positive business impact?
Are there any insights that lead to negative growth? Justify with specific reason.

Customer Engagement: The bar plot highlights the importance of engaging with owners of older vehicles to maximize response rates. Insurance companies can implement targeted outreach strategies, such as personalized communication or loyalty programs, to encourage owners of older vehicles to consider insurance options. By fostering positive relationships with this segment of customers, insurers can enhance customer retention and loyalty over time.

Overall, the insights from the bar plot of mean response rates for different categories of 'Vehicle_Age' enable insurance companies to develop more effective marketing strategies, customize products to meet customer needs, assess risk accurately, and enhance customer engagement, ultimately driving business growth and profitability.

#### Chart - 9-Multivariate Violin Plot of Response by Vehicle Age and Vehicle Damage:
"""

# Chart - 9 visualization code
plt.figure(figsize=(10, 6))
sns.violinplot(x='Vehicle_Age', y='Response', hue='Vehicle_Damage', data=df, split=True, palette='Set2')
plt.title('Response by Vehicle Age and Vehicle Damage')
plt.xlabel('Vehicle Age')
plt.ylabel('Response')
plt.legend(title='Vehicle Damage')
plt.show()

"""##### 1. Why did you pick the specific chart?

A violin plot is a type of visualization that combines aspects of a box plot and a kernel density plot to show the distribution of data across different categories. In this case, the violin plot with x='Vehicle_Age', y='Response', and hue='Vehicle_Damage' visualizes the relationship between the response variable and vehicle age, with the additional differentiation based on whether vehicle damage is present or not.

##### 2. What is/are the insight(s) found from the chart?

Spread of Violins: The spread of the violin plot indicates the distribution of responses within each category of vehicle age. If the violin is wider, it suggests a higher variability in responses, whereas a narrower violin suggests lower variability.

Comparison between Vehicle Damage Categories: By differentiating between vehicle damage (yes or no), the violin plot allows for a visual comparison of response distributions within each category of vehicle age. If the green (vehicle damage = yes) violin has a broader spread compared to the orange (vehicle damage = no) violin, it suggests that there may be more variability in responses among vehicles with damage.

Relationship with Vehicle Age: Additionally, the position and shape of the violins along the x-axis (vehicle age) provide insights into how the response variable varies across different age groups of vehicles, and whether this relationship differs based on the presence or absence of vehicle damage.

##### 3. Will the gained insights help creating a positive business impact?
Are there any insights that lead to negative growth? Justify with specific reason.

The presence of vehicle damage influences customer response across different vehicle age groups. Insurance companies can leverage this information to assess risk more accurately and adjust pricing strategies accordingly. Vehicles with a history of damage may pose a higher risk of future claims, necessitating higher premiums or more stringent underwriting criteria. Conversely, vehicles without damage may be perceived as lower risk, allowing insurers to offer more competitive rates to attract customers.Overall, the insights from the violin plot enable insurance companies to make data-driven decisions that enhance customer engagement, improve risk management, and drive business growth. By understanding how the response variable relates to vehicle age and damage status, insurers can optimize their operations and offerings to better meet the needs of their customers while minimizing risks and maximizing profitability.

#### Chart - 10 - Correlation Heatmap
"""

# Correlation Heatmap visualization code
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix Heatmap')
plt.show()

"""##### 1. Why did you pick the specific chart?

A Multivariate Heatmap of a Correlation Matrix is an effective way to visualize the relationships between multiple numerical variables. Each cell in the heatmap represents the correlation coefficient between two variables, with colors indicating the strength and direction of the correlation.

##### 2. What is/are the insight(s) found from the chart?

Policy Sale Channel and Previously Insured Correlation: The heatmap likely shows a significant correlation between the policy sale channel and the previously insured status. The correlation coefficient indicates the strength and direction of this relationship. A positive correlation suggests that certain policy sale channels may be associated with a higher likelihood of customers being previously insured, while a negative correlation suggests the opposite. This insight is valuable for understanding how different sales channels may attract different types of customers, which can inform marketing strategies and resource allocation.

Age and Response Correlation: The heatmap also indicates a correlation, albeit a weaker one, between age and the response variable. This suggests that there may be some relationship between a customer's age and their response to whatever prompt or question is being analyzed. While the correlation may not be as strong as the one between policy sale channel and previously insured status, it still provides valuable information for understanding customer behavior and preferences. This insight can be used to tailor marketing strategies and product offerings to different age groups, as well as for predictive modeling and feature selection purposes.

## ***5. Hypothesis Testing***

### Based on your chart experiments, define three hypothetical statements from the dataset. In the next three questions, perform hypothesis testing to obtain final conclusion about the statements through your code and statistical testing.

Hypothetical Statement 1: Younger individuals (age < 30) are more likely to have a driving license compared to older individuals (age >= 30).

Hypothetical Statement 2: The mean annual premium for individuals with vehicle damage is higher than the mean annual premium for individuals without vehicle damage.

Hypothetical Statement 3: There is no significant difference in the mean age of individuals who responded positively (1) and negatively (0) to insurance offers.

### Hypothetical Statement - 1 [chi-square test]

#### 1. State Your research hypothesis as a null hypothesis and alternate hypothesis.

Null Hypothesis (H0): There is no significant difference in the proportion of individuals with a driving license between younger and older age groups.

Alternate Hypothesis (H1): Younger individuals (age < 30) are more likely to have a driving license compared to older individuals (age >= 30).

If the p-value is less than the significance level (e.g., 0.05), we reject the null hypothesis, suggesting that there is a significant difference in the proportion of individuals with a driving license between younger and older age groups.

#### 2. Perform an appropriate statistical test.

> Indented block
"""

# Perform Statistical Test to obtain P-Value
# Statement 1: Hypothesis test for proportions
contingency_table = pd.crosstab(data['Age'] < 30, data['Driving_License'])
chi2_stat, p_val, _, _ = stats.chi2_contingency(contingency_table)
print("Statement 1 - Chi-square Statistic:", chi2_stat)
print("Statement 1 - p-value:", p_val)

"""##### Which statistical test have you done to obtain P-Value?

Statement 1, we can perform a hypothesis test for proportions (chi-square test).With such a small p-value (much smaller than the common significance level of 0.05), we reject the null hypothesis. Therefore, we have sufficient evidence to conclude that there is a significant difference in the proportion of individuals with a driving license between younger (age < 30) and older (age >= 30) age groups.

##### Why did you choose the specific statistical test?

I chose the chi-square test for Statement 1 because it is appropriate for testing the association between two categorical variables, particularly when the variables represent counts or frequencies in different categories. In this case, the variables are "Age" (< 30 vs. >= 30) and "Driving_License" (presence or absence of a driving license).

The chi-square test evaluates whether there is a significant difference in the proportions of individuals with a driving license between younger and older age groups. It assesses whether the observed frequencies in each category are significantly different from what would be expected under the null hypothesis of no association between the variables.

The p-value obtained from the chi-square test (4.908599437258652e-121) is extremely small, indicating strong evidence against the null hypothesis. Therefore, we reject the null hypothesis and conclude that there is a significant association between age and driving license status, with younger individuals (< 30 years old) being more likely to have a driving license compared to older individuals (>= 30 years old).

### Hypothetical Statement - 2 [independent samples t-test]

#### 1. State Your research hypothesis as a null hypothesis and alternate hypothesis.

Null Hypothesis (H0): There is no significant difference in the mean annual premium between individuals with vehicle damage and individuals without vehicle damage.
Alternate Hypothesis (H1): The mean annual premium for individuals with vehicle damage is higher than the mean annual premium for individuals without vehicle damage.

If the p-value is less than the significance level, we reject the null hypothesis, indicating that there is a significant difference in the mean annual premium between individuals with vehicle damage and individuals without vehicle damage.

#### 2. Perform an appropriate statistical test.
"""

# Perform Statistical Test to obtain P-Value
# Statement 2: Hypothesis test for means (Independent samples t-test)
mean_annual_premium_damage = data[data['Vehicle_Damage'] == 'Yes']['Annual_Premium']
mean_annual_premium_no_damage = data[data['Vehicle_Damage'] == 'No']['Annual_Premium']
t_stat, p_val = stats.ttest_ind(mean_annual_premium_damage, mean_annual_premium_no_damage, equal_var=False)
print("Statement 2 - t-statistic:", t_stat)
print("Statement 2 - p-value:", p_val)

"""##### Which statistical test have you done to obtain P-Value?

The specific statistical test chosen for Statement 2 is the independent samples t-test.In this case, the p-value obtained (7.49e-09) is very small, indicating strong evidence against the null hypothesis. Therefore, we reject the null hypothesis and conclude that there is a statistically significant difference in the mean annual premium between individuals with vehicle damage and individuals without vehicle damage. This conclusion is supported by the large t-statistic (5.78), which indicates the magnitude of the difference between the two groups relative to the variability within each group.

##### Why did you choose the specific statistical test?

In Statement 2, we are comparing the mean annual premium between two independent groups: individuals with vehicle damage and individuals without vehicle damage. The t-test allows us to assess whether the observed difference in mean annual premiums between these two groups is statistically significant or if it could have occurred by random chance alone.

The independent samples t-test assumes that the data within each group are normally distributed and that the variance of the two groups is approximately equal. However, if the assumption of equal variances is violated, we can use the Welch's t-test, which is a modification of the independent samples t-test that does not assume equal variances.

### Hypothetical Statement - 3 [independent samples t-test]

#### 1. State Your research hypothesis as a null hypothesis and alternate hypothesis.

Null Hypothesis (H0): There is no significant difference in the mean age of individuals who responded positively (1) and negatively (0) to insurance offers.

Alternate Hypothesis (H1): There is a significant difference in the mean age of individuals who responded positively (1) and negatively (0) to insurance offers.

 If the p-value is less than the significance level, we reject the null hypothesis, concluding that there is a significant difference in the mean age of individuals who responded positively and negatively to insurance offers.

#### 2. Perform an appropriate statistical test.
"""

# Perform Statistical Test to obtain P-Value
# Statement 3: Hypothesis test for means (Independent samples t-test)
mean_age_response_1 = data[data['Response'] == 1]['Age']
mean_age_response_0 = data[data['Response'] == 0]['Age']
t_stat, p_val = stats.ttest_ind(mean_age_response_1, mean_age_response_0, equal_var=False)
print("Statement 3 - t-statistic:", t_stat)
print("Statement 3 - p-value:", p_val)

"""##### Which statistical test have you done to obtain P-Value?

The specific statistical test chosen for Statement 3 is also the independent samples t-test. This test is appropriate when comparing the means of two independent groups to determine if there is a statistically significant difference between them.

##### Why did you choose the specific statistical test?

In Statement 3, we are comparing the mean age of individuals who responded positively (1) and negatively (0) to insurance offers. The t-test allows us to assess whether the observed difference in mean ages between these two groups is statistically significant or if it could have occurred by random chance alone.

Just like in Statement 2, the independent samples t-test assumes that the data within each group are normally distributed and that the variance of the two groups is approximately equal. The large t-statistic (83.99) and the extremely small p-value (0.0) obtained in this case indicate strong evidence against the null hypothesis.

## ***6. Feature Engineering & Data Pre-processing***

### 1. Handling Missing Values
"""

# Handling Missing Values & Missing Value Imputation
missing_values = df.isnull().sum()
print("Missing Values:\n", missing_values)

"""#### What all missing value imputation techniques have you used and why did you use those techniques?

There are no missing values in the dataset so the imputation process is skipped

### 2. Handling Outliers
"""

# Handling Outliers & Outlier treatments

# Visualize numerical features using box plots to identify outliers
numerical_features = df.select_dtypes(include=['float64', 'int64'])
plt.figure(figsize=(12, 6))
sns.boxplot(data=numerical_features)
plt.title("Box Plot of Numerical Features")
plt.xticks(rotation=45)
plt.show()

# Handle outliers by capping them
def cap_outliers(df, columns, threshold=0.95):
    capped_data = df.copy()
    for col in columns:
        upper_bound = capped_data[col].quantile(threshold)
        capped_data[col] = capped_data[col].apply(lambda x: upper_bound if x > upper_bound else x)
    return capped_data

# Apply outlier treatment
columns_to_cap = ['Annual_Premium', 'Driving_License','Response']
data_capped = cap_outliers(df, columns_to_cap)

# Visualize box plots after outlier treatment
plt.figure(figsize=(12, 6))
sns.boxplot(data=data_capped[columns_to_cap])
plt.title("Box Plot of Numerical Features after Outlier Treatment")
plt.xticks(rotation=45)
plt.show()

"""##### What all outlier treatment techniques have you used and why did you use those techniques?

Visualizing the numerical features using box plots to identify outliers,then implementa function cap_outliers to cap outliers in specific numerical columns based on a specified threshold.
And choosing to **cap outliers** because it helps in reducing the impact of extreme values without completely removing them, preserving some information from the original dataset.

**Removing Outliers:**

Suitable when outliers are clearly errors or anomalies.
May result in loss of information if valid data points are also removed.

**Transforming Outliers:**

Apply transformations such as log transformation, square root transformation, or Box-Cox transformation to reduce the impact of outliers.
Useful when outliers are skewing the distribution of the data.

**Capping Outliers:**

Set a threshold value beyond which outliers are capped.
Helps in reducing the impact of extreme values without removing them entirely.

### 3. Categorical Encoding
"""

# Encode your categorical columns
categorical_columns = df.select_dtypes(include=['object']).columns

# One-Hot Encoding
one_hot_encoder = OneHotEncoder(drop='first', sparse=False)
data_one_hot_encoded = one_hot_encoder.fit_transform(df[categorical_columns])
data_one_hot_encoded = pd.DataFrame(data_one_hot_encoded, columns=one_hot_encoder.get_feature_names_out(categorical_columns))
data_encoded_one_hot = pd.concat([df.drop(categorical_columns, axis=1), data_one_hot_encoded], axis=1)

# Label Encoding
label_encoder = LabelEncoder()
data_label_encoded = df.copy()
for col in categorical_columns:
    data_label_encoded[col] = label_encoder.fit_transform(df[col])

# Print the encoded data
print("One-Hot Encoded Data:")
print(data_encoded_one_hot.head())
print("\nLabel Encoded Data:")
print(data_label_encoded.head())

"""#### What all categorical encoding techniques have you used & why did you use those techniques?

For categorical encoding, we commonly use techniques like One-Hot Encoding and Label Encoding. The choice of technique depends on the nature of the categorical variables and the requirements of the downstream analysis or modeling task.

**One-Hot Encoding:**

Converts categorical variables into binary vectors where each category is represented by a binary column.
Suitable for categorical variables with no inherent ordinal relationship and when the number of categories is not too large.
Preserves the distinction between categories but may lead to high dimensionality if the number of unique categories is large.

**Label Encoding:**

Assigns a unique integer to each category in the categorical variable.
Suitable for ordinal categorical variables where the categories have a meaningful order.
Results in a single numerical column, reducing dimensionality compared to one-hot encoding.

# Used both techniques because:

One-Hot Encoding is suitable when there is no inherent ordinal relationship between categories and when the number of unique categories is not too large.
Label Encoding is suitable for ordinal categorical variables where the categories have a meaningful order and when we want to reduce dimensionality compared to one-hot encoding.

### 4. Textual Data Preprocessing
(It's mandatory for textual dataset i.e., NLP, Sentiment Analysis, Text Clustering etc.)

#### 1. Expand Contraction
"""

# Expand Contraction

"""#### 2. Lower Casing"""

# Lower Casing

"""#### 3. Removing Punctuations"""

# Remove Punctuations

"""#### 4. Removing URLs & Removing words and digits contain digits."""

# Remove URLs & Remove words and digits contain digits

"""#### 5. Removing Stopwords & Removing White spaces"""

# Remove Stopwords

# Remove White spaces

"""#### 6. Rephrase Text"""

# Rephrase Text

"""#### 7. Tokenization"""

# Tokenization

"""#### 8. Text Normalization"""

# Normalizing Text (i.e., Stemming, Lemmatization etc.)

"""##### Which text normalization technique have you used and why?

Answer Here.

#### 9. Part of speech tagging
"""

# POS Taging

"""#### 10. Text Vectorization"""

# Vectorizing Text

"""##### Which text vectorization technique have you used and why?

Answer Here.

### 4. Feature Manipulation & Selection

#### 1. Feature Manipulation
"""

# Manipulate Features to minimize feature correlation and create new features
# Feature Manipulation: Creating new feature 'Premium_Per_Age'
df['Premium_Per_Age'] = df['Annual_Premium'] / df['Age']

"""Created a new feature 'Premium_Per_Age' by dividing 'Annual_Premium' by 'Age', which could potentially capture the ratio of annual premium to age.

#### 2. Feature Selection
"""

# Select your features wisely to avoid overfitting

# Perform Feature Selection using SelectKBest
selector = SelectKBest(score_func=f_classif, k=5)
X_selected = selector.fit_transform(data_encoded_one_hot.drop('Response', axis=1), data_encoded_one_hot['Response'])

# Perform Feature Selection using Random Forest for feature importance ranking
rf_classifier = RandomForestClassifier()
rf_classifier.fit(data_encoded_one_hot.drop('Response', axis=1), data_encoded_one_hot['Response'])
feature_importances = rf_classifier.feature_importances_

# Print selected features
selected_features = data_encoded_one_hot.drop('Response', axis=1).columns[selector.get_support()]
print("Selected Features using SelectKBest:")
print(selected_features)

print("\nFeature Importances from Random Forest:")
print(dict(zip(data_encoded_one_hot.drop('Response', axis=1).columns, feature_importances)))

"""##### What all feature selection methods have you used  and why?

Random Forest Feature Importance Ranking: We used the feature importances obtained from the Random Forest classifier to rank the features based on their importance. Random Forest is a popular algorithm for feature selection because it inherently measures feature importance during training.

##### Which all features you found important and why?

Based on the feature importances, the following features are considered important:

'id': This feature seems to have the highest importance score, indicating that it contributes significantly to the model's prediction. However, it's important to note that 'id' might not be a meaningful predictor and could be an artifact of the dataset.

'Age': Age is another important feature with a relatively high importance score. This is common in many insurance-related datasets, as age often correlates with risk factors and insurance premiums.

'Vintage': Vintage, representing the number of days since the customer was associated with the company, also has a high importance score. This could indicate that customer loyalty or tenure plays a significant role in predicting their response to insurance offers.

'Annual_Premium': The annual premium is understandably an essential feature for insurance-related predictions, as it directly relates to the cost of insurance for the customer.

'Previously_Insured': Whether a customer was previously insured or not is also an important predictor. Customers who were previously insured may behave differently from those who were not.

'Region_Code': The region code also plays a role in predicting customer response. Different regions may have different insurance market dynamics, regulations, or customer behaviors.

##**why**
'Age' and 'Annual_Premium' are often important predictors in insurance-related datasets because they directly relate to risk assessment and pricing.
'Vintage' may indicate customer loyalty or engagement with the company, which could influence their response to offers.
'Previously_Insured' provides insights into the customer's history with insurance, affecting their likelihood of responding to new offers.
'Region_Code' may capture geographical variations in insurance markets, customer demographics, or regulatory environments, influencing response behavior.
'id', being the unique identifier, may have a high importance score due to its presence in the dataset, but it's typically not meaningful for prediction purposes and may be considered as noise.
It's important to interpret feature importance scores in the context of the specific problem and domain knowledge. While feature selection methods like Random Forest can provide valuable insights, they should be complemented with domain expertise and further analysis to ensure the selected features are meaningful and contribute to the model's interpretability and performance.

### 5. Data Transformation

#### Do you think that your data needs to be transformed? If yes, which transformation have you used. Explain Why?

Yes, data transformation may be necessary for various reasons, such as:

Normalization: Scaling numerical features to a similar scale, which helps algorithms converge faster and prevents certain features from dominating others.

Handling Skewness: Transforming skewed features to achieve a more symmetrical distribution, which can improve the performance of models that assume normality.

Handling Outliers: Applying transformations like logarithmic or power transformations to mitigate the impact of outliers on the model.

Encoding Categorical Variables: Converting categorical variables into numerical format using techniques like one-hot encoding or label encoding, which is often required by machine learning algorithms.

Depending on the specific characteristics of the data and the requirements of the modeling task, different transformations may be applied.

For this dataset, we've already performed one-hot encoding for categorical variables. However, we may consider applying other transformations such as normalization or handling skewness, especially for numerical features like 'Age' and 'Annual_Premium'.

Not all numerical columns need to be normalized. The decision to normalize numerical features depends on the context of the data and the requirements of the modeling task.
"""

# Transform Your data
from sklearn.preprocessing import MinMaxScaler

# Apply Min-Max scaling to numerical features
scaler = MinMaxScaler()
data_normalized = data_encoded_one_hot.copy()  # Assuming 'data_encoded_one_hot' is the encoded dataset
numerical_columns = ['Age', 'Annual_Premium', 'Vintage']
data_normalized[numerical_columns] = scaler.fit_transform(data_encoded_one_hot[numerical_columns])

"""Why Normalization?

**Uniform Scale:** Normalization scales numerical features to a similar range (usually [0, 1]), ensuring that no feature dominates due to its scale.
**Algorithm Sensitivity:** Many machine learning algorithms, such as neural networks and SVMs, are sensitive to the scale of input features. Normalization helps these algorithms converge faster and perform better.
Interpretability: Normalized features are easier to interpret since they all have the same scale.

By applying Min-Max scaling (a type of normalization), we ensure that numerical features are on a uniform scale, which can benefit the performance of various machine learning algorithms. Additionally, it aids in preventing features with larger magnitudes from dominating those with smaller magnitudes during model training.

### 6. Data Scaling
"""

# Initialize MinMaxScaler
scaler = MinMaxScaler()

# Scale numerical features
data_scaled = data_encoded_one_hot.copy()  # Make a copy of the original dataset
data_scaled[numerical_columns] = scaler.fit_transform(data_encoded_one_hot[numerical_columns])

# Print scaled data
print("Scaled Data:")
print(data_scaled.head())

"""##### Which method have you used to scale you data and why?
 I applied Min-Max scaling, also known as normalization, to scale the numerical features. Min-Max scaling scales the numerical features to a fixed range, typically [0, 1], by subtracting the minimum value and dividing by the range of each feature. This method was chosen for the following reasons:

Preservation of Relationships: Min-Max scaling preserves the relationships between the original values, ensuring that the relative differences between data points are maintained. This is important for maintaining the interpretability of the data.

Uniform Scale: By bringing all numerical features to the same scale, Min-Max scaling prevents features with larger magnitudes from dominating those with smaller magnitudes during model training. This helps algorithms converge faster and improves the stability of optimization algorithms.

Compatibility with Algorithms: Min-Max scaling is suitable for a wide range of machine learning algorithms, including linear regression, logistic regression, support vector machines, and artificial neural networks. Many of these algorithms perform better when input features are on a similar scale.

Simplicity: Min-Max scaling is a simple and straightforward method to implement. It involves subtracting the minimum value and dividing by the range, making it easy to understand and apply.

No Effect on Distribution Shape: Min-Max scaling does not change the shape of the distribution of the data. It only shifts and rescales the data linearly, ensuring that the distribution's properties remain unchanged.

However, it's essential to note that Min-Max scaling may not be suitable for all scenarios, particularly if the data contains outliers or if preserving the original distribution shape is critical. In such cases, alternative scaling methods like standardization (Z-score scaling) or robust scaling (using median and interquartile range) may be more appropriate. Ultimately, the choice of scaling method depends on the characteristics of the data and the requirements of the modeling task.

### 7. Dimesionality Reduction

##### Do you think that dimensionality reduction is needed? Explain Why?

Manageable Number of Features: The dataset contains only 12 columns, which is not excessively high-dimensional. In many cases, machine learning algorithms can handle datasets with this number of features without significant computational overhead or complexity issues.

Interpretability of Features: The features in the dataset appear to offer valuable insights into customer demographics, behavior, and preferences. Retaining these features in their original form can provide a clearer and more interpretable understanding of the factors influencing customer response and insurance purchases.

Potential Analysis Opportunities: The dataset offers various avenues for analysis, including understanding customer demographics, predicting response to marketing campaigns, and identifying factors influencing insurance purchases. Retaining the original features allows for a more comprehensive exploration of these analyses.

Model Performance Considerations: While dimensionality reduction can sometimes improve model performance, there is no explicit indication that model performance is hindered by the current dimensionality of the dataset. If models perform adequately without dimensionality reduction, there may be little benefit to reducing dimensionality further.

No Evidence of Collinearity or Redundancy: The insights provided do not suggest any significant issues with collinearity or redundancy among features. Dimensionality reduction techniques are often employed to mitigate these issues, but if they are not present in the dataset, there may be less justification for dimensionality reduction.

In summary, the decision to apply dimensionality reduction should be based on specific needs, constraints, and characteristics of the dataset. While dimensionality reduction can be beneficial in certain situations, it may not be immediately necessary if the dataset is manageable in size, features are interpretable, and there are no apparent issues with model performance or feature redundancy.

### 8. Data Splitting
"""

# Split your data to train and test. Choose Splitting ratio wisely.
from sklearn.model_selection import train_test_split

# Split the data into features (X) and target variable (y)
X = data_scaled.drop('Response', axis=1)  # Features
y = data_scaled['Response']  # Target variable

# Choose the splitting ratio wisely (e.g., 80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Print the shape of the training and testing sets
print("Shape of training set:", X_train.shape)
print("Shape of testing set:", X_test.shape)

"""##### What data splitting ratio have you used and why?

The 80-20 split strikes a balance between having sufficient data for model training and having enough data for evaluation. With 80% of the data allocated for training, the model has a substantial amount of data to learn patterns and relationships within the dataset. Meanwhile, reserving 20% of the data for testing allows for a robust evaluation of the trained model's performance.

### 9. Handling Imbalanced Dataset

##### Do you think the dataset is imbalanced? Explain Why.

Answer Here.
"""

from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
import pandas as pd

# Assuming 'X' contains the features and 'y' contains the target variable
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize SMOTE
smote = SMOTE(random_state=42)

# Apply SMOTE to the training data only
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# Print the shape of the resampled training data
print("Shape of resampled training set:")
print(X_train_resampled.shape, y_train_resampled.shape)

# Now you can use X_train_resampled and y_train_resampled for training your model

"""##### What technique did you use to handle the imbalance dataset and why? (If needed to be balanced)

Balancing Classes: The dataset provided had a significant class imbalance, with one class (labeled 'No') vastly outnumbering the other class (labeled 'Yes'). This class imbalance can lead to biased model predictions, where the model may tend to favor the majority class.

Preservation of Information: SMOTE addresses the class imbalance by generating synthetic samples for the minority class, effectively increasing its representation in the dataset. Unlike simple oversampling techniques that duplicate existing minority class instances, SMOTE creates synthetic samples that are interpolated between similar instances, preserving the underlying characteristics and distributions of the minority class.

No Loss of Information: By generating synthetic samples, SMOTE helps prevent the loss of information that may occur with undersampling techniques, where instances from the majority class are discarded. This ensures that valuable information from the minority class is retained in the dataset.

Enhanced Model Learning: By balancing the class distribution, SMOTE enables the model to learn from both classes more effectively, leading to better generalization performance on unseen data. Models trained on balanced datasets are less likely to be biased towards the majority class and can make more accurate predictions for both classes.

Overall, I chose to use SMOTE because it effectively addresses the class imbalance issue in the dataset while preserving the original data's characteristics and improving the model's ability to learn from minority class instances.

## ***7. ML Model Implementation***

### ML Model - 1
"""

# ML Model - 1 Implementation
# Assuming 'X' contains the features and 'y' contains the target variable
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Logistic Regression model
model = LogisticRegression(random_state=42)

# Fit the model to the training data
model.fit(X_train, y_train)

# Predict on the testing data
y_pred = model.predict(X_test)

# Evaluate the model performance
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("Accuracy Score:", accuracy_score(y_test, y_pred))

"""#### 1. Explain the ML Model used and it's performance using Evaluation metric Score Chart."""

# Visualizing evaluation Metric Score chart
# Define classes and evaluation metric scores
classes = [0, 1]
precision = [0.88, 0]  # Precision scores for classes 0 and 1
recall = [1, 0]  # Recall scores for classes 0 and 1
f1_score = [0.93, 0]  # F1-score scores for classes 0 and 1

# Set width of bars
barWidth = 0.25

# Set position of bar on X axis
r1 = np.arange(len(precision))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]

# Make the plot
plt.figure(figsize=(10, 6))
plt.bar(r1, precision, color='blue', width=barWidth, edgecolor='grey', label='Precision')
plt.bar(r2, recall, color='orange', width=barWidth, edgecolor='grey', label='Recall')
plt.bar(r3, f1_score, color='green', width=barWidth, edgecolor='grey', label='F1-score')

# Add xticks on the middle of the group bars
plt.xlabel('Class', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(precision))], classes)
plt.ylabel('Score')
plt.title('Evaluation Metric Scores by Class')

# Create legend & Show graphic
plt.legend()
plt.show()

"""#### 2. Cross- Validation & Hyperparameter Tuning"""

# ML Model - 1 Implementation with hyperparameter optimization techniques (i.e., GridSearch CV, RandomSearch CV, Bayesian Optimization etc.)

# Perform k-fold cross-validation
scores = cross_val_score(model, X_train, y_train, cv=5)  # 5-fold cross-validation

# Print cross-validation scores
print("Cross-Validation Scores:", scores)
print("Mean CV Score:", np.mean(scores))

model = LogisticRegression(max_iter=1000, random_state=42)

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Define hyperparameters grid
param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100]}

# Initialize GridSearchCV
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')  # 5-fold cross-validation

# Fit GridSearchCV to the training data
grid_search.fit(X_train, y_train)

# Get best hyperparameters
best_params = grid_search.best_params_
print("Best Hyperparameters:", best_params)

# Get best model
best_model = grid_search.best_estimator_

"""##### Which hyperparameter optimization technique have you used and why?

Based on the hyperparameter tuning results and cross-validation scores, we have obtained the best hyperparameter for the logistic regression model, which is C=0.001.

Explanation:

Best Hyperparameters: The hyperparameter tuning process identified C=0.001 as the best regularization parameter for the logistic regression model. The C parameter controls the strength of regularization, with smaller values indicating stronger regularization.

Cross-Validation Scores: The cross-validation scores obtained from 5-fold cross-validation are as follows: [0.87802158, 0.87802158, 0.87803598, 0.87803598, 0.8729193]. The mean cross-validation score is approximately 0.877. These scores represent the accuracy of the model on different subsets of the training data.

Interpretation:

The mean cross-validation score of approximately 0.877 indicates that, on average, the logistic regression model achieves an accuracy of around 87.7% on unseen data when evaluated using cross-validation. This suggests that the model generalizes well to new data and is not overfitting to the training data.

The identified value of C=0.001 suggests that a relatively low level of regularization is sufficient to achieve optimal performance for this logistic regression model. This may indicate that the model is not overly complex and does not require strong regularization to prevent overfitting.

Overall, the hyperparameter tuning process and cross-validation results provide confidence in the performance and generalization ability of the logistic regression model for the given dataset.

##### Have you seen any improvement? Note down the improvement with updates Evaluation metric Score Chart.

From the updated evaluation metric score chart, we can observe a slight improvement in the mean cross-validation score after hyperparameter tuning. The mean cross-validation score increased from approximately 0.875 to 0.877, indicating a slight enhancement in the model's performance.

### ML Model - 2

#### 1. Explain the ML Model used and it's performance using Evaluation metric Score Chart.
"""

# Visualizing evaluation Metric Score chart
# Initialize the Random Forest classifier
model_rf = RandomForestClassifier(random_state=42)

# Fit the model to the training data
model_rf.fit(X_train, y_train)

# Predict on the testing data
y_pred_rf = model_rf.predict(X_test)

# Evaluate the model performance
print("Classification Report:")
print(classification_report(y_test, y_pred_rf))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_rf))
print("Accuracy Score:", accuracy_score(y_test, y_pred_rf))

"""#### 2. Cross- Validation & Hyperparameter Tuning"""

# ML Model - 1 Implementation with hyperparameter optimization techniques (i.e., GridSearch CV, RandomSearch CV, Bayesian Optimization etc.)
# Perform k-fold cross-validation
scores_rf = cross_val_score(model_rf, X_train, y_train, cv=5)  # 5-fold cross-validation

# Print cross-validation scores
print("Cross-Validation Scores:", scores_rf)
print("Mean CV Score:", np.mean(scores_rf))

from scipy.stats import randint

# Number of trees
n_estimators = [50, 80, 100]

# Maximum depth of trees
max_depth = [4, 6, 8]

# Minimum number of samples required to split a node
min_samples_split = [50, 100, 150]

# Minimum number of samples required at each leaf node
min_samples_leaf = [40, 50]

# Define hyperparameter distributions
param_distributions = {
    'n_estimators': n_estimators,
    'max_depth': max_depth,
    'min_samples_split': min_samples_split,
    'min_samples_leaf': min_samples_leaf
}

# Initialize RandomizedSearchCV
randomized_search_rf = RandomizedSearchCV(model_rf, param_distributions=param_distributions, n_iter=10, cv=5, scoring='accuracy', random_state=42)

# Fit RandomizedSearchCV to the training data
randomized_search_rf.fit(X_train, y_train)

# Get best hyperparameters
best_params_rf = randomized_search_rf.best_params_
print("Best Hyperparameters:", best_params_rf)

# Retrieve the best model from the randomized search
best_model_rf = randomized_search_rf.best_estimator_

# Perform k-fold cross-validation with the best model
scores_rf = cross_val_score(best_model_rf, X_train, y_train, cv=5)  # 5-fold cross-validation

# Print cross-validation scores
print("Cross-Validation Scores:", scores_rf)
print("Mean CV Score:", np.mean(scores_rf))

"""##### Which hyperparameter optimization technique have you used and why?

I used the RandomizedSearchCV technique for hyperparameter optimization. RandomizedSearchCV randomly samples a subset of hyperparameter combinations from the specified distributions, which makes it more efficient than GridSearchCV, especially for large search spaces.
RandomizedSearchCV is preferred when:

The hyperparameter search space is large.
There is limited computational resources.
A good-enough, rather than the best, set of hyperparameters is acceptable.

##### Have you seen any improvement? Note down the improvement with updates Evaluation metric Score Chart.

With the cross-validation scores obtained after hyperparameter tuning and cross-validation, we observe a consistent performance across all folds with scores ranging around 0.878. The mean cross-validation score is approximately 0.878, which indicates that the model is performing consistently well across different subsets of the training data.

This mean cross-validation score suggests that the model has good generalization performance and is likely to perform similarly on unseen data. Therefore, we can conclude that the hyperparameter tuning and cross-validation process have resulted in a stable and robust model with improved performance compared to the initial model evaluation.

#### 3. Explain each evaluation metric's indication towards business and the business impact pf the ML model used.

Precision: Precision measures the proportion of correctly predicted positive cases (True Positives) among all predicted positive cases (True Positives + False Positives). In a business context, precision indicates the accuracy of the model in identifying positive cases. Higher precision means fewer false positives, which can lead to cost savings and improved resource allocation.

Recall: Recall, also known as sensitivity or true positive rate, measures the proportion of correctly predicted positive cases (True Positives) among all actual positive cases (True Positives + False Negatives). In a business context, recall indicates the ability of the model to capture all positive cases. Higher recall means fewer false negatives, which can lead to better identification of potential opportunities or risks.

F1-score: F1-score is the harmonic mean of precision and recall and provides a balance between the two metrics. It takes into account both false positives and false negatives. F1-score is particularly useful when the class distribution is imbalanced. A higher F1-score indicates better overall performance of the model in terms of precision and recall.

Accuracy: Accuracy measures the proportion of correctly predicted cases (both True Positives and True Negatives) among all cases. While accuracy is a commonly used metric, it may not be the most suitable for imbalanced datasets, as it can be influenced by the majority class. Nonetheless, it provides a general indication of the overall correctness of the model's predictions.

By understanding and optimizing these evaluation metrics, businesses can make informed decisions about resource allocation, risk management, and strategic planning based on the predictions made by the machine learning model.

### ML Model - 3
"""

# ML Model - 3 Implementation
# Initialize the Gradient Boosting Classifier
model_gb = GradientBoostingClassifier(random_state=42)

# Fit the model on the training data
model_gb.fit(X_train, y_train)

# Predict on the testing data
y_pred_gb = model_gb.predict(X_test)

# Evaluate the performance of the model
print("Classification Report:")
print(classification_report(y_test, y_pred_gb))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_gb))

accuracy_gb = accuracy_score(y_test, y_pred_gb)
print("Accuracy Score:", accuracy_gb)

"""#### 1. Explain the ML Model used and it's performance using Evaluation metric Score Chart.

The machine learning model used in this case is the Gradient Boosting Classifier. Gradient Boosting is an ensemble learning technique that builds a sequence of weak learners (typically decision trees) in a sequential manner. Each new weak learner is trained to correct the errors made by the combination of the existing learners.

The performance of the Gradient Boosting Classifier, as evaluated using the classification report and confusion matrix, is as follows:

Classification Report:

Precision: Precision is the ratio of correctly predicted positive observations to the total predicted positives. In this case, the precision for class 0 (negative class) is 0.88, indicating that out of all the predicted negatives, 88% were actually negative. However, for class 1 (positive class), the precision is 0.00, indicating that the model did not correctly predict any true positives.
Recall: Recall, also known as sensitivity or true positive rate, is the ratio of correctly predicted positive observations to the all observations in actual class. The recall for class 0 is 1.00, meaning that all actual negatives were correctly predicted. However, the recall for class 1 is 0.00, indicating that the model failed to correctly predict any true positives.
F1-score: F1-score is the harmonic mean of precision and recall. It provides a balance between precision and recall. The F1-score for class 0 is 0.93, while for class 1 it is 0.00.
Support: Support is the number of actual occurrences of the class in the specified dataset. In this case, the support for class 0 is 66699, and for class 1 it is 9523.
Confusion Matrix:

The confusion matrix shows the counts of true positive, false positive, true negative, and false negative predictions made by the model. In this case, the confusion matrix indicates that all instances of class 0 were correctly predicted as class 0 (true negatives), but the model failed to predict any instances of class 1 (all predictions are false negatives).
Accuracy Score:

The accuracy score measures the proportion of correctly classified instances out of all instances. In this case, the accuracy score is 0.875, indicating that the model correctly predicted 87.5% of the instances.
Overall, while the model achieved high accuracy due to correctly predicting the majority class (class 0), it performed poorly in terms of precision, recall, and F1-score for the minority class (class 1). This indicates that the model has a significant imbalance issue and is not effectively capturing the positive class. Further investigation and potentially rebalancing techniques are needed to improve the model's performance on the minority class.
"""

# Visualizing evaluation Metric Score chart
# Define classes and corresponding evaluation metrics
classes = ['Class 0', 'Class 1']
precision = [0.88, 0.00]
recall = [1.00, 0.00]
f1_score = [0.93, 0.00]

# Create subplots
fig, ax = plt.subplots(figsize=(8, 6))

# Plot precision, recall, and F1-score
bar_width = 0.2
index = np.arange(len(classes))
ax.bar(index, precision, bar_width, label='Precision', color='b')
ax.bar(index + bar_width, recall, bar_width, label='Recall', color='g')
ax.bar(index + 2*bar_width, f1_score, bar_width, label='F1-score', color='r')

# Add labels, title, and legend
ax.set_xlabel('Classes')
ax.set_ylabel('Scores')
ax.set_title('Evaluation Metric Scores by Class')
ax.set_xticks(index + bar_width)
ax.set_xticklabels(classes)
ax.legend()

# Show plot
plt.tight_layout()
plt.show()

"""#### 2. Cross- Validation & Hyperparameter Tuning"""

# Perform k-fold cross-validation with the Gradient Boosting Classifier
scores_cv = cross_val_score(model_gb, X_train, y_train, cv=5, scoring='accuracy')

# Print cross-validation scores
print("Cross-Validation Scores:", scores_cv)
print("Mean CV Score:", np.mean(scores_cv))

# Define hyperparameters and their distributions
# Number of trees
n_estimators = [50, 80, 100]

# Maximum depth of trees
max_depth = [4, 6, 8]

# Minimum number of samples required to split a node
min_samples_split = [50, 100, 150]

# Minimum number of samples required at each leaf node
min_samples_leaf = [40, 50]

# Define hyperparameter distributions
param_dist= {
    'n_estimators': n_estimators,
    'max_depth': max_depth,
    'min_samples_split': min_samples_split,
    'min_samples_leaf': min_samples_leaf
}

# Initialize the randomized search
randomized_search_gb = RandomizedSearchCV(model_gb, param_distributions=param_dist, n_iter=10, cv=3, scoring='f1', random_state=42)

# Perform randomized search
randomized_search_gb.fit(X_train, y_train)

# Print best hyperparameters
print("Best Hyperparameters:", randomized_search_gb.best_params_)

from sklearn.ensemble import GradientBoostingClassifier

# Initialize Gradient Boosting Classifier with best hyperparameters
best_model_gb = GradientBoostingClassifier(n_estimators=100, min_samples_split=150, min_samples_leaf=40, max_depth=8, random_state=42)

# Fit the model on the training data
best_model_gb.fit(X_train, y_train)

# Predict on the testing data
y_pred_gb = best_model_gb.predict(X_test)

# Evaluate the performance of the model
print("Classification Report:")
print(classification_report(y_test, y_pred_gb))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_gb))

accuracy_gb = accuracy_score(y_test, y_pred_gb)
print("Accuracy Score:", accuracy_gb)

"""##### Which hyperparameter optimization technique have you used and why?

The hyperparameter optimization technique used was Randomized Search, which randomly samples a specified number of hyperparameter combinations from the specified distributions. Randomized Search was chosen over Grid Search for faster execution, especially when dealing with a large hyperparameter search space.

##### Have you seen any improvement? Note down the improvement with updates Evaluation metric Score Chart.

In terms of improvement, after hyperparameter tuning, there was a slight improvement in the model's performance. The classification report showed a slightly higher precision, recall, and F1-score for the positive class compared to the initial model without hyperparameter tuning. However, the improvement was relatively small, indicating that further optimization or model adjustments may be necessary to achieve significant gains.

### 1. Which Evaluation metrics did you consider for a positive business impact and why?

Certainly, among the evaluation metrics mentioned, Precision would be particularly crucial for positive business impact in certain scenarios. Precision measures the accuracy of the positive predictions made by the model, which means it assesses the proportion of correctly predicted positive instances among all instances predicted as positive.

Here's why Precision is important for positive business impact:

Cost of False Positives: In many real-world scenarios, the cost associated with false positives (incorrectly predicting a negative instance as positive) can be significant. For example, in a medical diagnosis application, falsely diagnosing a healthy patient as having a disease could lead to unnecessary treatments, expenses, and psychological distress for the patient. Therefore, it's crucial to minimize false positives to avoid such negative consequences.

Customer Experience: False positives can also impact customer experience and satisfaction. For instance, in an e-commerce platform, recommending irrelevant or incorrect products to customers based on inaccurate predictions could lead to frustration and dissatisfaction, potentially driving customers away from the platform.

Resource Allocation: Precision is vital for optimizing resource allocation and decision-making processes. In scenarios where resources (such as sales efforts, marketing budgets, or medical interventions) need to be allocated efficiently, high precision ensures that resources are directed towards instances where they are most likely to have a positive impact.

Trust in Predictive Models: High precision instills trust and confidence in predictive models among stakeholders, including decision-makers, customers, and end-users. A model that consistently delivers accurate and reliable predictions with minimal false positives is more likely to be embraced and utilized effectively within the organization.

In summary, prioritizing Precision as an evaluation metric ensures that the model's positive predictions are trustworthy, impactful, and aligned with the business objectives. By minimizing false positives, businesses can enhance customer experience, optimize resource allocation, and build trust in their predictive models, ultimately leading to positive business outcomes.

### 2. Which ML model did you choose from the above created models as your final prediction model and why?

The chosen model appears to be a Gradient Boosting Classifier. Here's a description of the model based on the provided evaluation metrics:

Precision and Recall:

Precision for class 1 (positive class) is 0.54, indicating that when the model predicts a positive instance, it is correct approximately 54% of the time.
Recall for class 1 is 0.01, indicating that the model correctly identifies only 1% of the actual positive instances.
F1-Score:

The F1-score for class 1 is 0.03, which is the harmonic mean of precision and recall. It reflects the balance between precision and recall for the positive class.
Accuracy:

The overall accuracy of the model is 0.88, which means that it correctly predicts the class label for approximately 88% of the instances in the test set.
Confusion Matrix:

The confusion matrix shows the distribution of true positive, true negative, false positive, and false negative predictions. In this case, the majority of predictions (66590) belong to the true negative class (class 0), while only 129 predictions belong to the true positive class (class 1).
The model has a relatively high number of false negatives (9394), indicating instances of class 1 that were incorrectly predicted as class 0.
Macro and Weighted Averages:

The macro average of precision, recall, and F1-score provides an unweighted average across all classes, while the weighted average considers class imbalance by weighting each class's score by its support (the number of true instances for each class). In this case, both macro and weighted averages show similar results due to the balanced class distribution.
Based on these metrics, the chosen model (Gradient Boosting Classifier) demonstrates decent overall accuracy but struggles with identifying instances of the minority class (class 1) correctly, as indicated by its low recall and F1-score for class 1. This model may require further tuning or additional strategies to address the imbalance and improve performance on the positive class.

### 3. Explain the model which you have used and the feature importance using any model explainability tool?
"""

!pip install shap

import shap
# Get SHAP values
explainer = shap.Explainer(best_model_gb)
shap_values = explainer(X_test)

# Waterfall plot for the first observation
shap.plots.waterfall(shap_values[0])

"""The features "Vehicle Age" and "Vintage" are showing positive contributions in the SHAP waterfall plot, it means that these features are increasing the model's prediction compared to the baseline. Here's what it implies for each feature:

Vehicle Age: A positive contribution from the "Vehicle Age" feature suggests that as the age of the vehicle increases, the model predicts a higher likelihood of the event being predicted ( a customer purchasing insurance). This could mean that older vehicles are associated with a higher probability of the event occurring.

Vintage: Similarly, a positive contribution from the "Vintage" feature indicates that as the vintage (duration since inception or registration) of the customer's relationship with the company increases, the model predicts a higher probability of the event. This suggests that customers with longer-standing relationships are more likely to exhibit the behavior or outcome being predicted.

Understanding these positive contributions helps in interpreting the factors that influence the model's predictions positively. It provides insights into which features are driving the model's decision-making process and helps in understanding the relationships between the features and the predicted outcome.

### ***Congrats! Your model is successfully created and ready for deployment on a live server for a real user interaction !!!***

# **Conclusion**

Based on the evaluation of the three machine learning models trained on the dataset, the Gradient Boosting Classifier with the following hyperparameters yielded the most promising results:

n_estimators: 100
min_samples_split: 150
min_samples_leaf: 40
max_depth: 8
The model achieved an accuracy score of approximately 87.53% on the test data. However, the precision, recall, and F1-score for predicting the positive class (1) are relatively low, indicating that the model struggles to accurately classify positive instances.

Interpreting the model using SHAP (SHapley Additive exPlanations) values revealed that features such as "Vehicle Age" and "Vintage" have a positive impact on the model's predictions, suggesting that older vehicles and longer-standing customer relationships are associated with a higher likelihood of the predicted event (e.g., purchasing insurance).

In conclusion, while the Gradient Boosting Classifier model demonstrates good overall accuracy, further optimization may be needed to improve its performance in identifying positive instances. Additionally, the insights gained from the SHAP analysis can inform business decisions, such as targeting older vehicles and customers with longer relationships for insurance products or services.

### ***Hurrah! You have successfully completed your Machine Learning Capstone Project !!!***
"""
