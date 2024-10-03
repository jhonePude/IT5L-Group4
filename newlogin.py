import tkinter as tk
from tkinter import ttk, Tk, PhotoImage
from tkinter import messagebox
import runpy
import hashlib
import bcrypt
import os
import subprocess
from mysql.connector import Error
import mysql.connector 
from thisclass import myclass

from PIL import Image, ImageTk
import io
import sv_ttk 
import customtkinter
import darkdetect



try:
    connection = mysql.connector.connect(
        host='localhost',  
        database='inventory_system',
        user='root',
        password=''
    )

    if connection.is_connected():
        os.system('python loading.py')
        
        #entire frame
        main_frame = Tk()
        main_frame.geometry(f'{1000}x{460}+{200}+{100}')
        main_frame.title("LOGIN PAGE")
        main_frame.wm_attributes("-transparentcolor","grey")
        main_frame.resizable(False,False)
        
        icon = PhotoImage(file="login.png")  
        main_frame.iconphoto(False, icon)
        
######################################################################################################################
#CODE ABOVE IS THE ENTIRE FRAME CODE BELOW IS SECOND FRAME FOR SIGNN IN PAGE
######################################################################################################################################
        def create_signin_homepage():
          
            auto_delete_pages()   
          
            def on_focus_in(event):
     
                forgetpass1.configure(fg="blue")
        
            def on_focus_out(event):
            
                forgetpass1.configure(fg="black")
            
            homepage = myclass.hompageinsignin(frame_userinputs)
            
            text_var = tk.StringVar()
            text_var.set("USERNAME") 
            lbl_username = tk.Label(homepage, bg= "lightblue", textvariable=text_var, anchor=tk.W, font=("Arial Black", 10,"bold"), justify=tk.CENTER)
            lbl_username.pack()
            lbl_username.place(x=25, y=120, width=140,height=30)

            text_var = tk.StringVar()
            text_var.set("PASSWORD") 
            lbl_password = tk.Label(homepage, bg= "lightblue", textvariable=text_var, anchor=tk.W, font=("Arial Black", 10,"bold"), justify=tk.CENTER)
            lbl_password.pack()
            lbl_password.place(x=25, y=217, width=160,height=15)
            
            forget_var = tk.StringVar()
            forget_var.set("Forget Password") 
            forgetpass1 = tk.Label(homepage, bg= "lightblue", textvariable=forget_var, anchor=tk.W, font=("Arial", 8,"bold"), justify=tk.CENTER)
            forgetpass1.pack()
            forgetpass1.place(x=200, y=356)
            
            forgetpass1.bind("<Enter>",on_focus_in)
            forgetpass1.bind("<Leave>",on_focus_out)
        
            textfield1_username1= customtkinter.CTkEntry(homepage,height=45,width=290, text_color= "black",fg_color=("blue","white"),border_color= "#86739B",border_width=2,placeholder_text="Username" ,font=('Arial', 18),corner_radius=50)
            textfield1_username1.pack()
            textfield1_username1.place(x=25,y=150)

            textfield2_password2 = customtkinter.CTkEntry(homepage,height=45,width=290, text_color= "black",fg_color=("blue","white"),border_color= "#86739B",border_width=2,placeholder_text="Password",show ="•" ,font=('Arial', 18),corner_radius=50)
            textfield2_password2.pack()
            textfield2_password2.place(x=25,y=240)
            
            def insidecheckbutton():
                myclass.save_accountsforrememberme(textfield1_username1,textfield2_password2,check_button)
             
            myclass.load_accountsforrememberme(textfield1_username1,textfield2_password2)
            
            check_button =tk.BooleanVar()
            checkbutton = tk.Checkbutton(homepage,variable = check_button,text="Remember Me", command = insidecheckbutton,bg= "light blue", activebackground="light blue", font=("Arial",8, "bold"))
            checkbutton.pack()
            checkbutton.place(x=25, y=355)
            
       
##########################################################################################################################################################################            
# CODE ABOVE IS FOR 2ND FRAME NA MAG SHOW SA 2ND USERNAME AND PASSWORD
##########################################################################################################################################################################            
            pandaopen = Image.open("pandaopen.png")                                      
            pandaopen.thumbnail((150, 120), Image.LANCZOS)
            pandaopen_pic = ImageTk.PhotoImage(pandaopen)

            pandaclose = Image.open("pandaclose.png")                                      
            pandaclose.thumbnail((150, 120), Image.LANCZOS)
            pandaclose_pic = ImageTk.PhotoImage(pandaclose)
            
                        
            def toggle_password1():
                
                    eyesopen1 = "EYES1.jpg" 
                    image_eyeopen1 = Image.open(eyesopen1)
                    new_size1 = (25, 25)  
                    resized_image1 = image_eyeopen1.resize(new_size1, Image.LANCZOS)
                    openeye_ctk_image = customtkinter.CTkImage(light_image=resized_image1)

                    eyesclose2 = "EYES2.jpg" 
                    image_eyeclose2 = Image.open(eyesclose2)
                    new_size2 = (25, 25)  
                    resized_image2 = image_eyeclose2.resize(new_size2, Image.LANCZOS)
                    closeeyes_ctk_image = customtkinter.CTkImage(light_image=resized_image2)
                    
                
                    if textfield2_password2.cget("show") == "•":
                        
                        textfield2_password2.configure(show="")
                        show_password_button.configure(image = openeye_ctk_image)
                        
                        pandaopen_label = tk.Label(frame_userinputs, image= pandaopen_pic,background="light blue")
                        pandaopen_label.pack()
                        pandaopen_label.place(x=108, y=10)
                        
                    else:
                        
                        textfield2_password2.configure(show="•")
                        show_password_button.configure(image = closeeyes_ctk_image)
                        
                        pandaclose_label = tk.Label(frame_userinputs, image= pandaclose_pic,background="light blue")
                        pandaclose_label.pack()
                        pandaclose_label.place(x=108, y=10)
            
            def on_click_login1():
                username = textfield1_username1.get()
                password = textfield2_password2.get()
                hushedpasword = hash_password1(password)
                
                # login logic inside
                myclass.user_login_on_click(username,password,hushedpasword,connection,main_frame)
                    
            def hash_password1(password):
                hash_object = hashlib.sha256(password.encode('utf-8'))
                return hash_object.hexdigest()


            eyesclose = "EYES2.jpg"  
            image_eyeclose = Image.open(eyesclose)
            new_size = (25, 25)  
            resized_image = image_eyeclose.resize(new_size, Image.LANCZOS)
            closeeye_ctk_image = customtkinter.CTkImage(light_image=resized_image)

            pandaclose = Image.open("pandaclose.png")                                      
            pandaclose.thumbnail((150, 120), Image.LANCZOS)
            pandaclose_pic = ImageTk.PhotoImage(pandaclose)
            pandaclose_label = tk.Label(frame_userinputs, image= pandaclose_pic,background="light blue")
            pandaclose_label.pack()
            pandaclose_label.place(x=108, y=10)

            show_password_button = customtkinter.CTkButton(homepage ,bg_color="White",hover_color="white",fg_color=("White","White"),text="",image=closeeye_ctk_image ,cursor="hand2",font=("Arial", 18), command=toggle_password1,width=8,corner_radius=100)
            show_password_button.pack()
            show_password_button.place(x=255, y=246)
            
            login_button = customtkinter.CTkButton(homepage, cursor="hand2", text="Sign In",text_color= "black",fg_color=("white","#05d7ff"), font = ("Arial",18), command = on_click_login1, width=65,corner_radius=50)
            login_button.configure(width=290, height=40)
            login_button.pack()
            login_button.place(x = 25, y = 305)
            
###################################################################################################################################
#CODE ABOVE IS FOR 2ND FRAME ANIMATIONS SA EYES AND PANDA SA 2ND FRAME AND TOGGLE
############################################################################################################################
     #frame sa create account
        frame1_createAcc_signIn = tk.Frame(main_frame)
        frame1_createAcc_signIn.pack(side=tk.LEFT)
        frame1_createAcc_signIn.pack_propagate(False)
        frame1_createAcc_signIn.configure(width=650, height=600)
        
        #background image sa naay sign in and create account button
        frame1_bg_image = Image.open("reconnect.png")                                      
        frame1_bg_image.thumbnail((1200, 600), Image.LANCZOS)
        frame1_bg_backgroundphoto = ImageTk.PhotoImage(frame1_bg_image)
        
        frame1_bg_label = tk.Label(frame1_createAcc_signIn, image= frame1_bg_backgroundphoto,bd=0)
        frame1_bg_label.pack()
        frame1_bg_label.place(x=-5,y=-30)
        
        def create_Acc_homepage():
            auto_delete_pages()
            
            createaccountpage = tk.Frame(frame_userinputs, bg= "light blue")
            createaccountpage.pack(side=tk.LEFT)
            createaccountpage.pack_propagate(False)
            createaccountpage.configure(width=650, height=600)
        
            def on_click_reg():
                
                user_input = textfield1_signup_username.get()
                user_pass = textfield2_signup_password.get()
                user_email = textfield3_signup_email.get()
                hushedpasword = hash_password(user_pass)
                
            
                if user_input == "" or user_pass == "" or user_email == "":
                    messagebox.showerror("Error", "Please fill in all fields.")
                    
                elif not myclass.validate_email(user_email):
                    messagebox.showerror("Error", "Please fill email with @yahoo.com or @gmail.com")

                else:
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO `account`(`userID`, `userName`,userEmail, `userPass`) VALUES (%s, %s, %s, %s)",('', user_input, user_email ,hushedpasword))
                    connection.commit()
                    messagebox.showinfo("Account Creation","Account Created")
                    
                    textfield1_signup_username.delete(0, tk.END)
                    textfield2_signup_password.delete(0, tk.END)
                    textfield3_signup_email.delete(0, tk.END)
                    
                    create_signin_homepage()
            
            text_var0 = tk.StringVar()
            text_var0.set("Create Account") 
            lbl_username0 = tk.Label(createaccountpage, bg= "lightblue", textvariable=text_var0, anchor=tk.W, font=("Arial Black", 17,"bold"), justify=tk.CENTER)
            lbl_username0.pack()
            lbl_username0.place(x=70, y=30, width=200,height=30)
            
            text_var1 = tk.StringVar()
            text_var1.set("USERNAME") 
            lbl_username1 = tk.Label(createaccountpage, bg= "lightblue", textvariable=text_var1, anchor=tk.W, font=("Arial Black", 10,"bold"), justify=tk.CENTER)
            lbl_username1.pack()
            lbl_username1.place(x=25, y=90, width=140,height=30)
            
            text_var2 = tk.StringVar()
            text_var2.set("PASSWORD") 
            lbl_password2 = tk.Label(createaccountpage, bg= "lightblue", textvariable=text_var2, anchor=tk.W, font=("Arial Black", 10,"bold"), justify=tk.CENTER)
            lbl_password2.pack()
            lbl_password2.place(x=25, y=187, width=160,height=15)
            
            text_var3 = tk.StringVar()
            text_var3.set("E-MAIL") 
            lbl_password3 = tk.Label(createaccountpage, bg= "lightblue", textvariable=text_var3, anchor=tk.W, font=("Arial Black", 10,"bold"), justify=tk.CENTER)
            lbl_password3.pack()
            lbl_password3.place(x=25, y=275, width=160,height=15)
            
            textfield1_signup_username= customtkinter.CTkEntry(createaccountpage,height=45,width=290, text_color= "black",fg_color=("blue","white"),border_color= "#86739B",border_width=2,placeholder_text="Username" ,font=('Arial', 18),corner_radius=50)
            textfield1_signup_username.pack()
            textfield1_signup_username.place(x=25,y=120)

            textfield2_signup_password = customtkinter.CTkEntry(createaccountpage,height=45,width=290, text_color= "black",fg_color=("blue","white"),border_color= "#86739B",border_width=2,placeholder_text="Password",font=('Arial', 18),corner_radius=50)
            textfield2_signup_password.pack()
            textfield2_signup_password.place(x=25,y=210)
            
            textfield3_signup_email = customtkinter.CTkEntry(createaccountpage,height=45,width=290, text_color= "black",fg_color=("blue","white"),border_color= "#86739B",border_width=2,placeholder_text="Email" ,font=('Arial', 18),corner_radius=50)
            textfield3_signup_email.pack()
            textfield3_signup_email.place(x=25,y=295)

            register_button = customtkinter.CTkButton(createaccountpage, cursor="hand2", text="Register",text_color= "black",fg_color=("white","#05d7ff"), font = ("Arial",18), command = on_click_reg, width=65,corner_radius=50)
            register_button.configure(width=290, height=40)
            register_button.pack()
            register_button.place(x = 25, y = 365)

############################################################################################################################################################
#ALL CODES ABOVE  IS FOR THE CREATE ACCOUNT NA FRAME PAG GE PINDOT ANG CREATE ACCOUNT NA BUTTON
############################################################################################################################################################
       
        def auto_delete_pages():   
            #frame kung asa ang user information create account inputs
            for frame in frame_userinputs.winfo_children():
                frame.destroy()

############################################################################################################################################################
#ALL CODES BELOW IS PARA SA FiRST FRAME KUNG ASA MU POP UP AND LOGIN USERNAME AND PASSWORD PAG RUN NIMO
############################################################################################################################################################
       
        pandaopen = Image.open("pandaopen.png")                                      
        pandaopen.thumbnail((150, 120), Image.LANCZOS)
        pandaopen_pic = ImageTk.PhotoImage(pandaopen)

        pandaclose = Image.open("pandaclose.png")                                      
        pandaclose.thumbnail((150, 120), Image.LANCZOS)
        pandaclose_pic = ImageTk.PhotoImage(pandaclose)

################################################################################################################################
#frame kung asa and 1st username and password inputs
################################################################################################################################
        frame_userinputs = tk.Frame(main_frame)
        frame_userinputs.configure(width=500, height=600, bg="lightblue",highlightbackground="#6790C9",highlightthickness="10",highlightcolor="lightblue")
        frame_userinputs.pack(side=tk.LEFT)
        frame_userinputs.pack_propagate(False)
        
        def toggle_password():
                eyesopen1 = "EYES1.jpg" 
                image_eyeopen1 = Image.open(eyesopen1)
                new_size1 = (25, 25)  
                resized_image1 = image_eyeopen1.resize(new_size1, Image.LANCZOS)
                openeye_ctk_image = customtkinter.CTkImage(light_image=resized_image1)

                eyesclose2 = "EYES2.jpg" 
                image_eyeclose2 = Image.open(eyesclose2)
                new_size2 = (25, 25)  
                resized_image2 = image_eyeclose2.resize(new_size2, Image.LANCZOS)
                closeeyes_ctk_image = customtkinter.CTkImage(light_image=resized_image2)
                
            
                if textfield2_password.cget("show") == "•":
                    
                    textfield2_password.configure(show="")
                    show_password_button.configure(image = openeye_ctk_image)
                    
                    
                    pandaopen_label = tk.Label(frame_userinputs, image= pandaopen_pic,background="light blue")
                    pandaopen_label.pack()
                    pandaopen_label.place(x=108, y=10)
                    
                else:
                    
                    textfield2_password.configure(show="•")
                    show_password_button.configure(image = closeeyes_ctk_image)
                
                    
                    pandaclose_label = tk.Label(frame_userinputs, image= pandaclose_pic,background="light blue")
                    pandaclose_label.pack()
                    pandaclose_label.place(x=108, y=10)
                    
                    
        def on_click_login():
            username = textfield1_username.get()
            password = textfield2_password.get()
            hushedpasword = hash_password(password)
            
            #1st frame kung asa and 1st username and password inputs (process para maka login inside)
            myclass.user_login_on_click(username,password,hushedpasword,connection,main_frame)
        
        def hash_password(password):
            hash_object = hashlib.sha256(password.encode('utf-8'))
            return hash_object.hexdigest()
        
        
        
        def on_focus_in(event):
     
            forgetpass.configure(fg="blue")
        
        def on_focus_out(event):
            
             forgetpass.configure(fg="black")
    
        ########################################################################################################################                
        #CODES ABOVE IS SA 1ST FRAME NA HASHING PASSWORD, SHOWPASSWORD ANIMATION, AND ANIMATION SA PANDA SA LOGIN
        ########################################################################################################################
       

        text_var = tk.StringVar()
        text_var.set("USERNAME") 
        lbl_username = tk.Label(frame_userinputs, bg= "lightblue", textvariable=text_var, anchor=tk.W, font=("Arial Black", 10,"bold"), justify=tk.CENTER)
        lbl_username.pack()
        lbl_username.place(x=25, y=120, width=140,height=30)

        text_var = tk.StringVar()
        text_var.set("PASSWORD") 
        lbl_password = tk.Label(frame_userinputs, bg= "lightblue", textvariable=text_var, anchor=tk.W, font=("Arial Black", 10,"bold"), justify=tk.CENTER)
        lbl_password.pack()
        lbl_password.place(x=25, y=217, width=160,height=15)
        
   
        forget_var = tk.StringVar()
        forget_var.set("Forget Password") 
        forgetpass = tk.Label(frame_userinputs, bg= "lightblue", textvariable=forget_var, anchor=tk.W, font=("Arial", 8,"bold"), justify=tk.CENTER)
        forgetpass.pack()
        forgetpass.place(x=200, y=356)
       

             
        forgetpass.bind("<Enter>",on_focus_in)
        forgetpass.bind("<Leave>",on_focus_out)
        

        textfield1_username= customtkinter.CTkEntry(frame_userinputs,height=45,width=290, text_color= "black",fg_color=("blue","white"),border_color= "#86739B",border_width=2,placeholder_text="Username" ,font=('Arial', 18),corner_radius=50)
        textfield1_username.pack()
        textfield1_username.place(x=25,y=150)

        textfield2_password = customtkinter.CTkEntry(frame_userinputs,height=45,width=290, text_color= "black",fg_color=("blue","white"),border_color= "#86739B",border_width=2,placeholder_text="Password",show ="•" ,font=('Arial', 18),corner_radius=50)
        textfield2_password.pack()
        textfield2_password.place(x=25,y=240)
       
        def insidecheckbutton():
             myclass.save_accountsforrememberme(textfield1_username,textfield2_password,check_button)
             
        myclass.load_accountsforrememberme(textfield1_username,textfield2_password)
        
        check_button =tk.BooleanVar()
        checkbutton = tk.Checkbutton(frame_userinputs,variable = check_button,text="Remember Me", command = insidecheckbutton,bg= "light blue", activebackground="light blue", font=("Arial",8, "bold"))
        checkbutton.pack()
        checkbutton.place(x=25, y=355)
        
        login_button = customtkinter.CTkButton(frame_userinputs, cursor="hand2", text="Sign In",text_color= "black",fg_color=("white","#05d7ff"), font = ("Arial",18), command = on_click_login, width=65,corner_radius=50)
        login_button.configure(width=290, height=40)
        login_button.pack()
        login_button.place(x = 25, y = 305)
        
        createAcc_button = customtkinter.CTkButton(frame1_createAcc_signIn, bg_color= "#9c7995", cursor="hand2", text="Create Account", text_color= "white",fg_color=("black","black"), font = ("Arial",18,"bold"), command = create_Acc_homepage, border_spacing=3, width=65,corner_radius=50)
        createAcc_button.configure(width=115, height=45)
        createAcc_button.place(x = 480, y = 408)
        
        sign_inButton = customtkinter.CTkButton(frame1_createAcc_signIn, bg_color= "#907ca4", cursor="hand2", text="Sign In", text_color= "white",fg_color=("#05d7ff","#05d7ff"), font = ("Arial",18,"bold"), command = create_signin_homepage, border_spacing=3,width=65,corner_radius=50)
        sign_inButton.configure(width=115, height=45)
        sign_inButton.place(x = 508, y = 355)

        eyesclose = "EYES2.jpg"  
        image_eyeclose = Image.open(eyesclose)
        new_size = (25, 25)  
        resized_image = image_eyeclose.resize(new_size, Image.LANCZOS)
        closeeye_ctk_image = customtkinter.CTkImage(light_image=resized_image)


        pandaclose = Image.open("pandaclose.png")                                      
        pandaclose.thumbnail((150, 120), Image.LANCZOS)
        pandaclose_pic = ImageTk.PhotoImage(pandaclose)
        pandaclose_label = tk.Label(frame_userinputs, image= pandaclose_pic,background="light blue")
        pandaclose_label.pack()
        pandaclose_label.place(x=108, y=10)


        show_password_button = customtkinter.CTkButton(frame_userinputs ,bg_color="White",hover_color="white",fg_color=("White","White"),text="",image=closeeye_ctk_image ,cursor="hand2",font=("Arial", 18), command=toggle_password,width=8,corner_radius=100)
        show_password_button.pack()
        show_password_button.place(x=255, y=246)


######################################################################################################################

        main_frame.mainloop()

except Error as e:
        messagebox.showerror("MySQL Connection Error", f"Error connecting to MySQL: {e}")
