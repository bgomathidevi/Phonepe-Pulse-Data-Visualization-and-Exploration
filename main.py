import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo
import requests
import plotly.graph_objs as go


# Define options globally
options = ["--select--",
           "Top 10 states based on year and amount of transaction",
           "List 10 states based on type and amount of transaction",
           "Top 5 Transaction_Type based on Transaction_Amount",
           "Top 10 Registered-users based on States and District",
           "Top 10 Districts based on states and Count of transaction",
           "List 10 Districts based on states and amount of transaction",
           "List 10 Transaction_Count based on Districts and states",
           "Top 10 RegisteredUsers based on states and District"]

# Setting up page configuration
st.set_page_config(
    page_title="Phonepe Pulse Data Visualization | By Gomathidevi",
    layout="wide"
)


# Creating connection with MySQL Workbench
mydb = sql.connect(
    host="localhost",
    user="root",
    password="595959kgms@karthidevi",
    database="phonepe_pulse"
)
mycursor = mydb.cursor(buffered=True)

# Creating option menu in the sidebar
with st.sidebar:
    selected = option_menu(
        "Menu",
        ["About", "Home", "Basic insights", "Top Charts", "Explore Map", "Contact"],
        icons=["info-circle", "house", "graph-up-arrow", "bar-chart-line", "map-marker-alt", "at"],
        menu_icon="menu-button-wide",
        default_index=0,
        styles={"nav-link": {"font-size": "17px", "text-align": "left", "margin": "-2px", "--hover-color": "#000000"},
                "nav-link-selected": {"background-color": "#000000"}}
    )


#----------------About-----------------------#
if selected == "About":
    st.image(Image.open("G:\\PROJECT\\project_2_PHONEPAY\\phonepe.png"), width=500)
    col1,col2 = st.columns(2)
    
    with col1:
        
        st.write("---")
        st.markdown("""
            <div style='text-align: justify;'>
                <h3 style='font-size: 20px;'>
                    The Indian digital payments story has truly captured the world's imagination. 
                    From the largest towns to the remotest villages, there is a payments revolution being driven by the 
                    penetration of mobile phones, mobile internet, and states-of-the-art payments infrastructure built as 
                    Public Goods championed by the central bank and the government.
                    Founded in December 2015, PhonePe has been a strong beneficiary of the API-driven digitization of payments in India.
                    When PhonePe started, they were constantly looking for granular and definitive data sources on digital payments in India.
                </h3>
            </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.write("---")

    with col2:
        st.video("G:\\PROJECT\\project_2_PHONEPAY\\pulse-video.mp4")
    
    col1,col2 = st.columns(2)
    with col1:
        st.image(Image.open("G:\\PROJECT\\project_2_PHONEPAY\\top.jpeg"),width = 400)
    with col2:
        st.write("THE BEAT OF PHONEPE")
        st.subheader("Phonepe became a leading digital payments company")
    

#----------------Home----------------------#
mycursor = mydb.cursor()

# execute a SELECT statement
mycursor.execute("SELECT * FROM agg_trans")

# fetch all rows
rows = mycursor.fetchall()
from streamlit_extras.add_vertical_space import add_vertical_space

if selected == "Home":

    st.image(Image.open("G:\\PROJECT\\project_2_PHONEPAY\\phonepe.png"), width=500)
    col1, col2 = st.columns(2)
    with col1:
        st.write("---")
        st.subheader(
            """
            **PhonePe** has been a pioneer in the Indian digital payments landscape since its establishment in December 2015 
            by Sameer Nigam, Rahul Chari, and Burzin Engineer. Leveraging the Unified Payments Interface (UPI) technology, 
            PhonePe introduced its app to the market in August 2016, revolutionizing the way individuals and businesses 
            conduct financial transactions.
            
            Under the ownership of Flipkart, a subsidiary of Walmart, PhonePe has expanded its reach and offerings, 
            emerging as a leader in India's fintech industry. With a strong emphasis on user experience and technological 
            innovation, PhonePe continues to evolve its platform, providing consumers with convenient and efficient 
            payment solutions.
            
            Through strategic partnerships and a relentless commitment to customer satisfaction, PhonePe has established 
            itself as a key player in India's digital payments landscape, driving financial inclusion and fostering 
            economic growth.
            """
        )
        st.write("---")
        st.write("---")
        
    with col2:
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
        st.video("G:\\PROJECT\\project_2_PHONEPAY\\upi.mp4")




#---------------------TOP CHARTS -----------------#
if selected == "Top Charts":
    st.markdown("## :blue[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.info(
                """
                #### LEADERBOARD :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                )
# Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="small")
        
        with col1:
            st.markdown("### :blue[State]")
            mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.qualitative.Set1,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.markdown("### :blue[District]")
            mycursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Top 10',
                             color_discrete_sequence=px.colors.qualitative.Dark24,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col3:
            st.markdown("### :blue[Pincode]")
            mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='Pincode',
                             title='Top 10',
                             color_discrete_sequence=px.colors.qualitative.Bold,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
# Top Charts - USERS          
    if Type == "Users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        
        with col1:
            st.markdown("### :green[Brands]")
        
            mycursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
            fig = px.bar(df,
                            title='Top 10',
                            x="Total_Users",
                            y="Brand",
                            orientation='h',
                            color='Avg_Percentage',
                            color_continuous_scale=px.colors.sequential.Viridis)
            st.plotly_chart(fig,use_container_width=True)   
    
        with col2:
            st.markdown("### :green[District]")
            mycursor.execute(f"select district, sum(Registered_User) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Viridis)
            st.plotly_chart(fig,use_container_width=True)
              
        with col3:
            st.markdown("### :green[Pincode]")
            mycursor.execute(f"select Pincode, sum(Registered_Users) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Viridis,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col4:
            st.markdown("### :green[State]")
            mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Viridis,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

            

#---------------------EXPLORE DATA -----------------#
if selected == "Explore Map":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)
    
# EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :red[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :red[Overall State Data - Transactions Count]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(float)
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
            
            
# BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :red[Top Payment Type]")
        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)
        
# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :navyblue[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        mycursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
        
# EXPLORE DATA - USERS      
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df2 = pd.read_csv('Statenames.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_Users',
                  color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :navyblue[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        mycursor.execute(f"select State,year,quarter,District,sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)




#---------------------Basic Insights -----------------#


if selected == "Basic insights":
    
    st.write("----")
    selected_option = st.selectbox("Select an option", options)
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.info(
                """
                #### Let's know some basic insights about the data :
                - Top 10 states based on year and amount of transaction,
                - List 10 states based on type and amount of transaction,
                - Top 5 Transaction_Type based on Transaction_Amount,
                - Top 10 Registered-users based on States and District,
                - Top 10 Districts based on states and Count of transaction,
                - List 10 Districts based on states and amount of transaction,
                - List 10 Transaction_Count based on Districts and states,
                - Top 10 RegisteredUsers based on states and District
                """,icon="🔍"
                )
    

    ##1
    if selected_option == "Top 10 states based on year and amount of transaction":
        # Main page content
        st.write("### Top 10 states based on year and amount of transaction")
        query = f"SELECT State, SUM(Transaction_amount) AS Total_Transaction_Amount FROM agg_trans WHERE Year={Year} AND Quarter={Quarter} GROUP BY State ORDER BY Total_Transaction_Amount DESC LIMIT 10"
        mycursor.execute(query)
        result = mycursor.fetchall()
        
        # Display result in the first column
        col1, col2 = st.columns(2)
        with col1:
            st.write(pd.DataFrame(result, columns=["State", "Total Transaction Amount"]), use_container_width=True)
        with col2:   
            df = pd.DataFrame(result, columns=["State", "Total Transaction Amount"])

        # Plotting the graph
            fig = px.bar(df, x="Total Transaction Amount", y="State", orientation='h', title="Top 10 States by Transaction Amount")
        
        # Customize the layout
            fig.update_layout(
                xaxis_title="Total Transaction Amount",
                yaxis_title="State",
                yaxis=dict(autorange="reversed"),  # Reverse the y-axis to display states from top to bottom
                margin=dict(l=0, r=0, t=30, b=0)  # Adjust margin to fit the title properly
            )
        
        # Display the plot
            st.plotly_chart(fig, use_container_width=True)


    ##2

    elif selected_option == "List 10 states based on type and amount of transaction":
        # Main page content
        st.write("### List 10 states based on type and amount of transaction")
        query = f"SELECT State, SUM(Transaction_amount) AS Total_Transaction_Amount FROM agg_trans WHERE Year={Year} GROUP BY State ORDER BY Total_Transaction_Amount DESC LIMIT 10"
        mycursor.execute(query)
        result = mycursor.fetchall()
        
        # Display result in the first column
        col1, col2 = st.columns(2)
        with col1:
            st.write(pd.DataFrame(result, columns=["State", "Total Transaction Amount"]), use_container_width=True)

        # Display bar chart in the second column
        with col2:
            st.write("### Bar chart")
            if result:
                df_result = pd.DataFrame(result, columns=["State", "Total Transaction Amount"])
                fig = px.bar(df_result, x='State', y='Total Transaction Amount', title=f'Total Transaction Amount by State for Year {Year}')
                st.plotly_chart(fig, use_container_width=True)

    ##3

    elif selected_option == "Top 5 Transaction_Type based on Transaction_Amount":
        # Main page content
        st.write("### Top 5 Transaction Types based on Transaction Amount")
        query = ("SELECT Transaction_type, SUM(Transaction_amount) AS Total_Transaction_Amount FROM agg_trans GROUP BY Transaction_type ORDER BY Total_Transaction_Amount DESC LIMIT 5")
        mycursor.execute(query)
        result = mycursor.fetchall()
        
        # Display result in the first column
        col1, col2 = st.columns(2)
        with col1:
            st.write(pd.DataFrame(result, columns=["Transaction Type", "Total Transaction Amount"]), use_container_width=True)
            
        with col2:
            df = pd.DataFrame(result, columns=["Transaction Type", "Total Transaction Amount"])
            
            # Plotting the graph
            fig = go.Figure(data=go.Scatterpolar(
                r=df["Total Transaction Amount"],
                theta=df["Transaction Type"],
                fill='toself'
            ))
            
            # Customize the layout
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max(df["Total Transaction Amount"]) + 1000]  # Adjust range for better visualization
                    )
                ),
                title="Top 5 Transaction Types by Transaction Amount (Radar Chart)"
            )
            
            # Display the plot
            st.plotly_chart(fig, use_container_width=True)


        



###4

    elif selected_option == "Top 10 Registered-users based on States and District":
        st.write(f"### Top 10 Registered Users based on States and District for Year {Year} and Quarter {Quarter}")
        query = f"""
                SELECT State, District, SUM(Registered_user) AS Total_Registered_Users 
                FROM map_user 
                WHERE Year = {Year} AND Quarter = {Quarter}
                GROUP BY State, District 
                ORDER BY Total_Registered_Users DESC 
                LIMIT 10
                """
        mycursor.execute(query)
        result = mycursor.fetchall()
        
        # Display result in the first column
        col1, col2 = st.columns(2)
        with col1:
            
            st.write(pd.DataFrame(result, columns=["State", "District", "Total Registered Users"]), use_container_width=True)
       
            



    ##5
    elif selected_option == "Top 10 Districts based on states and Count of transaction":
        # Main page content
        st.write(f"### Top 10 Districts based on states and Count of transaction for Year {Year} and Quarter {Quarter}")
        query = f"""
                SELECT DISTINCT State, District, SUM(Count) AS Total_Count
                FROM map_trans
                
                GROUP BY State, District
                ORDER BY State, Total_Count DESC
                LIMIT 10
                """
        
        mycursor.execute(query)
        result = mycursor.fetchall()
        
        # Display result in the first column
        col1,col2 = st.columns(2)
        with col1:
            df = pd.DataFrame(result, columns=["State", "District", "Total Transaction Count"])
            st.write(pd.DataFrame(result, columns=["State", "District", "Total Transaction Count"]), use_container_width=True)
            
        with col2:
            fig = go.Figure(go.Treemap(
                    labels=df['District'],
                    parents=df['State'],
                    values=df['Total Transaction Count']
            ))

            fig.update_layout(
                title_text=f'Top 10 Districts based on States and Count of Transaction for Year {Year} and Quarter {Quarter}'
            )

            st.plotly_chart(fig, use_container_width=True)
            



    ##6
    elif selected_option == "List 10 Districts based on states and amount of transaction":
        # Main page content
        st.write("### List 10 Districts based on states and amount of transaction")

        # Modify the query to include conditions for year and quarter
        query = f"""
                SELECT State, District, SUM(Amount) AS Total_Transaction_Amount
                FROM map_trans
                WHERE Year = {Year} AND Quarter = {Quarter}
                GROUP BY State, District
                ORDER BY Total_Transaction_Amount DESC
                LIMIT 10
                """
        mycursor.execute(query)
        result = mycursor.fetchall()
        
        # Display result in the first column
        col1, col2 = st.columns(2)
        with col1:
            df = pd.DataFrame(result, columns=["State", "District", "Total Transaction Amount"])
            st.write(pd.DataFrame(result, columns=["State", "District", "Total Transaction Amount"]), use_container_width=True)
        with col2:
            fig = px.imshow(df.pivot(index='State', columns='District', values='Total Transaction Amount'),
                    labels=dict(color="Total Transaction Amount"))

            fig.update_layout(
                title=f"Top 10 Districts based on States and Amount of Transaction for Year {Year} and Quarter {Quarter}",
                xaxis_title="District",
                yaxis_title="State"
            )

            st.plotly_chart(fig, use_container_width=True)


        
    ##7
    elif selected_option == "List 10 Transaction_Count based on Districts and states":
        
        # Main page content
        st.write("### List 10 Transaction_Count based on Districts and states")

        # Modify the query to include conditions for year and quarter
        query = f"""
                SELECT State, District, SUM(Count) AS Total_Transaction_Count
                FROM map_trans
                WHERE Year = {Year} AND Quarter = {Quarter}
                GROUP BY State, District
                ORDER BY Total_Transaction_Count DESC
                LIMIT 10
                """
        mycursor.execute(query)
        result = mycursor.fetchall()
        
        # Display result in the first column
        col1, col2 = st.columns(2)
        with col1:
            df = pd.DataFrame(result, columns=["State", "District", "Total Transaction Count"])
            st.write(pd.DataFrame(result, columns=["State", "District", "Total Transaction Count"]), use_container_width=True)
        with col2:
                # Plot the treemap
            fig = px.treemap(df, path=['State', 'District'], values='Total Transaction Count',
                    title=f"Top 10 Transaction Counts based on Districts and States for Year {Year} and Quarter {Quarter}")

            fig.update_layout(
                    margin=dict(t=50, l=0, r=0, b=0)
            )

            st.plotly_chart(fig, use_container_width=True)


    ##8
    elif selected_option == "Top 10 RegisteredUsers based on states and District":
       
        st.write("### Top 10 RegisteredUsers based on states and District")

        query = f"""
                SELECT State, District, SUM(Registered_user) AS Total_Registered_Users
                FROM map_user
                WHERE Year = {Year} AND Quarter = {Quarter}
                GROUP BY State, District
                ORDER BY Total_Registered_Users DESC
                LIMIT 10
                """
        mycursor.execute(query)
        result = mycursor.fetchall()
        
        # Display result in the first column
        col1, col2 = st.columns(2)
        with col1:
            
            df = pd.DataFrame(result, columns=["State", "District", "Total Registered Users"])
            st.write(pd.DataFrame(result, columns=["State", "District", "Total Registered Users"]), use_container_width=True)
        with col2:
            pivot_df = df.pivot(index="District", columns="State", values="Total Registered Users")


            # Plot the heatmap
            fig = go.Figure(data=go.Heatmap(
                z=pivot_df.values,
                x=pivot_df.columns,
                y=pivot_df.index,
                colorscale='Viridis'))

            fig.update_layout(
                title=f"Top 10 Registered Users based on States and Districts for Year {Year} and Quarter {Quarter}",
                xaxis_title="District",
                yaxis_title="State"
            )

            st.plotly_chart(fig, use_container_width=True)


#----------------------Contact---------------#




if selected == "Contact":
    name = "Gomathidevi B"
    mail = (f'{"Mail :"}  {"bgomathidevi@gmail.com"}')
    description = "An Aspiring DATA-SCIENTIST..!"
    social_media = {
        "GITHUB": "https://github.com/bgomathidevi",
        "LINKEDIN": "https://www.linkedin.com/in/gomathidevi-b-7a55691b9/"}
    
    st.title('Phonepe Pulse Data Visualization and Exploration')
    st.write("The goal of this project is to extract data from the Phonepe pulse Github repository, transform and clean the data, insert it into a MySQL database, and create a live geo visualization dashboard using Streamlit and Plotly in Python. The dashboard will display the data in an interactive and visually appealing manner, with at least 10 different dropdown options for users to select different facts and figures to display. The solution must be secure, efficient, and user-friendly, providing valuable insights and information about the data in the Phonepe pulse Github repository.")
    st.write("---")
    st.subheader(mail)
    st.write("#")
    




