import pandas as pd
import plotly.express as px
import streamlit as st
# from PIL import Image
import stat
import glob
import os
import PIL.Image
import datetime
import torch
import database as db 
from streamlit_option_menu import option_menu


st.set_page_config(page_title = "Covid Dashboard",
 page_icon = ":bar_chart:",
 layout = "wide")#to use the entire scree

def get_data_from_excel():
   df = pd.read_excel(
      io = 'data.xlsx',
      engine='openpyxl',
      sheet_name='country_wise_latest',
      usecols='A:O',
      nrows=187)
   return df

df = get_data_from_excel()


#---horizontal menu---#

selected = option_menu(
     menu_title = None,
     options = ["Home","Patient Information","Upload Image"],
     icons= ["house-fill","person-fill","cloud-upload-fill"],
     default_index = 0,
    orientation="horizontal",
   )






# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


#--Home---

if selected == "Home" :
  st.sidebar.markdown(f'<h1 style="color:#ffffff;font-size:24px;">{"Please Filer Here:"}</h1>', unsafe_allow_html=True)

  region = st.sidebar.selectbox(
      "Select the Region: ",
      options=df["WHO_Region"].unique(),
      # default=df["WHO_Region"].unique()
)

  df_selection = df.query(
         "WHO_Region == @region"

)
    
  # st.markdown(f'<h1 style="color:#c77dff;font-size:55px;">{"Covid Cases"}</h1>', unsafe_allow_html=True)
  # st.markdown("##")

  total_cases = int(df_selection["Confirmed"].sum())
  total_deaths = int(df_selection["Deaths"].sum())
  total_recovered = int(df_selection["Recovered"].sum())

  left_col,mid_col,right_col = st.columns(3)
  with left_col:
      st.subheader("Total no of confirmed Covid cases: ")
      st.subheader(total_cases)

  with mid_col:
      st.subheader("Total no of deaths: ")
      st.subheader(total_deaths)  
  with right_col:
      st.subheader("Total no of recovered Covid cases: ")
      st.subheader(total_recovered)

  st.markdown("---")


### BARCHART


  fig_active_cases = px.bar(
    
    x= df_selection["Active"],
    y= df_selection["Country"],
    
    orientation="h",
    title="<b>No of Active Cases</b>",

   color_discrete_sequence=["#c77dff"]


   
)

  fig_active_cases.update_yaxes(title="Countries")
  fig_active_cases.update_xaxes(title="Active cases")


  im = PIL.Image.open('lottie/rr.jpg')


  left,mid = st.columns(2)
  left.plotly_chart(fig_active_cases, use_container_width=True)
  mid.image(im)






  st.markdown("---")
  fig = px.pie(df_selection, values='Recovered / 100 Cases', names='Country',
             title='Recovered / 100 Cases',color_discrete_sequence=[
                                                                    "#5A189A","#7b2cbf","#9d4edd","#c77dff","#e0aaff","#3C096C","#240046","#FFFFFF"]
             )
  fig.update_traces(textposition='inside', textinfo='percent+label')
# fig.show()
# st.plotly_chart(fig)

  fig1 = px.pie(df_selection, values='Deaths / 100 Cases', names='Country',
             title='Deaths / 100 Cases',color_discrete_sequence=[
                                                                    "#5A189A","#7b2cbf","#9d4edd","#c77dff","#e0aaff","#3C096C","#240046","#FFFFFF"]
             )
             
  fig1.update_traces(textposition='inside', textinfo='percent+label')
# fig.show()
# st.plotly_chart(fig1)

  fig2 = px.pie(df_selection, values='Confirmed last week', names='Country',
             title='Confirmed last week',color_discrete_sequence=[
                                                                    "#5A189A","#7b2cbf","#9d4edd","#c77dff","#e0aaff","#3C096C","#240046","#FFFFFF"]
             
             )
  fig2.update_traces(textposition='inside', textinfo='percent+label')

  fig3 = px.pie(df_selection, values='1 week percent increase', names='Country',
             title='1 week percent increase',color_discrete_sequence=[
                                                                    "#5A189A","#7b2cbf","#9d4edd","#c77dff","#e0aaff","#3C096C","#240046","#FFFFFF"]
             
             )
  fig2.update_traces(textposition='inside', textinfo='percent+label')
# fig.show()


  left_column,mid_column = st.columns(2)
  left_column.plotly_chart(fig, use_container_width=True)
  mid_column.plotly_chart(fig1, use_container_width=True)
# right_column.plotly_chart(fig2, use_container_width=True)

  left,mid = st.columns(2)
  left.plotly_chart(fig2, use_container_width=True)
  mid.plotly_chart(fig3, use_container_width=True)


if selected == "Patient Information":
    st.header(f"Patient Information")
    with st.form("Entry_form", clear_on_submit=True):
     name = st.text_input('Name')
     age = st.number_input('Age',step = 0)
     dob = st.date_input(
     "Date of Birth",datetime.date(2023, 1, 1))
     phone = st.number_input('Phone Number',step = 0)
     aadhar = st.number_input('Aadhar Number',step = 0)
     gender = st.selectbox('Gender',("Male","Female"))
     pincode = st.number_input('Pincode',step = 0)
     address = st.text_area('Address')
     submitted = st.form_submit_button("Save Data")
     stdob = str(dob)
     if submitted:
           db.insert_period(name,age,stdob,phone,aadhar,gender,pincode,address)
           st.success("Data Saved!")

    st.markdown("""
    <style>
    button.step-up {display: none;}
    button.step-down {display: none;}
    div[data-baseweb] {border-radius: 4px;}
    </style>""",
    unsafe_allow_html=True)
    
    
if selected == "Upload Image":
 nom=""
 @st.cache_data
 def load_image(image_file):
    img = PIL.Image.open(image_file)
    new_width = 400
    new_height = 400
    img = img.resize((new_width, new_height), PIL.Image.LANCZOS)
    return img
 
 

# Model
 def getmodel(image_file):
  model = torch.hub.load('ultralytics/yolov5', 'custom', 'best.pt')
  model.conf = 0.45   
  model.agnostic = True    
  model.iou = 0.2                                               
# Images
  # img = image_file # or file, Path, PIL, OpenCV, numpy, list

# Inference
  results = model(image_file)


# Results
# results.show()  # or .show(), .save(), .crop(), .pandas(), etc.
 
  pandasbox=len(results.pandas().xyxy[0]) 
  print("number: "+str(pandasbox))
  res = results.save(labels=False)
  pandasbox=len(results.pandas().xyxy[0]) 
# print("number: "+str(pandasbox))
  return res,str(pandasbox)

 
 uploaded_file = st.file_uploader("Choose an image to upload")
 
 st.write('')
 one,two,three = st.columns(3)
 with one:
       getans = st.button("Preview")
 with two:
       st.write("")
 with three:
       getans1 = st.button("Detect")

 coll1, coll2,coll3 = st.columns(3)
 st.write('')
 if getans:
    if uploaded_file is not None:
      

      with coll1:
        st.image(load_image(uploaded_file))

     
         

 with coll2:
     st.write('')
 if getans1:
     with coll3:
        try:
            # file_path = glob.glob('runs\detect\exp')
            # print(os.path.exists(file_path))
            
            # for f in file_path:
            #   os.chmod(f , stat.S_IWRITE)
            #   os.remove(f)
             ans,nom = getmodel(load_image(uploaded_file))
             res = st.image(ans)

          
           
        except AttributeError:
            im = PIL.Image.open('runs\detect\exp\image0.jpg')
            coll2.image(im)
            
    
st.write('The number of bacteria clusters are:' + nom)         

    

    
    
    
