from mysql.connector import Error
import mysql.connector 
from tkinter import *
import tkinter as tk
from tkinter import ttk, Tk, filedialog
from tkinter import messagebox 
from thisclass import myclass
from PIL import Image, ImageTk
import sv_ttk #sun valley themed package from github
import customtkinter
import datetime
import os
import base64
import PyQt5
import tkinter.font as tkFont
import customtkinter


try:
    connection = mysql.connector.connect(
        host='localhost',  
        database='inventory_system',
        user='root',
        password=''
    )

    if connection.is_connected():
        frame = Tk()     
        frame.geometry(f'{1366}x{768}+{-7}+{0}')
        frame.title("INVENTORY SYSTEM")
        frame.resizable(False, False)
        
        icon = PhotoImage(file="logistics.png")  # Replace with your icon file path
        frame.iconphoto(False, icon)
      
###################################################################################################
        
        style = ttk.Style()
        tree = myclass.create_treeview(frame,style)
    
        cursor = connection.cursor()
        # cursor.execute("SELECT * FROM stocks")  
        # rows = cursor.fetchall()  
        
        with open('username.txt', 'r') as f:
            current_username = f.read().strip()
        
        cursor.execute("SELECT userID FROM account WHERE userName = %s", (current_username,))
        userIDD = cursor.fetchone()
        
        if userIDD:  # Check if the user was found
            userID = int(userIDD[0])  # Extract the userID

            # Query with INNER JOIN to get products for the specific user
            query = """
               SELECT s.Product_ID, s.Product_Name, s.Product_Price, s.Product_Quantity, s.Product_Added_Date, s.Product_Expiration, a.userName
                FROM account a
                INNER JOIN stocks s ON a.userID = s.userID
                WHERE a.userID = %s;
            """
            cursor.execute(query, (userID,))  # Use the fetched userID
            
        rows = cursor.fetchall()
        
        for item in tree.get_children():
            tree.delete(item)

        for row in rows:
            tree.insert("", "end", values=row)
        cursor.close()
        
        
########################################################################################################### 
        def add_on_click():
            row_daata = []    
    
            selected_user = combo.get()        

            prdct_id,prdct_name,prdct_price,prdct_qty, prdct_expire = myclass.num_checker_get_values(textfield1,textfield2,textfield3,textfield5,textfield7)
                
            myclass.add_row_on_click(prdct_id, prdct_name, prdct_price,prdct_qty, prdct_expire, tree, row_daata,userID,combo,connection,textfield1,textfield2,textfield3,textfield5,textfield7)
    

        ############################################################################################
        def row_on_click(event):

            selected_row = tree.selection()
            
            # myclass.selected_row_on_click(textfield1, textfield2, textfield3, selected_row, tree, connection)
            
            if selected_row:
                item = tree.item(selected_row)
                values = item['values']
                prduct_id = item['values'][0]
                
                
                with open('stocksimages.txt', 'r') as imagesfile:
                
        
                    for line in imagesfile:
                        saved_image_path = line.strip().split(',')  # Assuming each line is formatted like "prdct_id,filepath"
                        if saved_image_path[0] == str(prduct_id):  # Compare product ID
                            image_file_path = saved_image_path[1]  # Get the corresponding image file path
                            try:
                                # Load and display the image
                                 image = Image.open(image_file_path)
                                 image = image.resize((200, 200))  # Resize image as needed
                                 photo = ImageTk.PhotoImage(image)
                        
                                # Update the label with the new image
                                 label5.config(image=photo)
                                 label5.image = photo  # Keep a reference to avoid garbage collection
                            except Exception as e:
                                print(f"Error loading image: {e}")
                
                        
                myclass.row_clicked_auto_delete_texfields(values,textfield1,textfield2,textfield3,textfield5,textfield7)
                
        ##############################################################################################
        def delete_on_click():
            selected_row = tree.selection()
            if selected_row:
            
                myclass.delete_selected_row(textfield1,textfield2,textfield3,textfield5,textfield7,selected_row, connection,tree)
                
                label5.config(image='')  
                label5.image = None  
            
            else:
                messagebox.showerror("Error", "Select A Row First! ")  
                
        ##########################################################################################################        

        def update_on_click():
                
            if textfield2.get() != "" and textfield3.get() != "":
                
                selected_row = tree.selection()
                myclass.updated_row_on_click(textfield1,textfield2,textfield3,textfield5,textfield7,selected_row, connection,tree)
            
            else:
                messagebox.showerror("Error", "Please Select A Row First")
                myclass.auto_delete_texfields(textfield1,textfield2,textfield3,textfield5,textfield7)
                
                    
        #####################################################################################################               
        def search_on_click():
            product_id = textfield4.get()
            textfield4.delete(0, tk.END)
            myclass.searchbox(product_id,tree,connection,label5,textfield1,textfield2,textfield3,textfield5,textfield7,combo)
            myclass.auto_delete_texfields(textfield1,textfield2,textfield3,textfield5,textfield7)
                        
            
    v_scrollbar = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree.configure(yscrollcommand=v_scrollbar.set)

    tree.pack(fill=tk.BOTH, expand=True)
    
    tree.bind("<ButtonRelease-1>", row_on_click)


###########################################################################################################
    # add combobox datas from textfile 
    try:
        
        with open('username.txt', 'r') as  f:
            current_username = f.read().strip()
            print(f"Currently LogIn: {current_username}")
        
    except FileNotFoundError:
            print("No username found.")
##################################################################################################################

    
    button_delete = tk.Button(frame,background="#05d7ff", foreground= "#020f12", activebackground= "#65e7ff", activeforeground="BLACK", highlightthickness=2, highlightbackground="#05d7ff", cursor="hand2", border="1", text="DELETE", font = ("Bahnschrift",11,"italic"), command = delete_on_click, highlightcolor="white")
    button_delete.pack(padx=10, pady=50)
    button_delete.place(x= 50,y=620)
    button_delete.config(height= 2, width=25)

    button_update = tk.Button(frame,background="#05d7ff", foreground= "#020f12", activebackground= "#65e7ff", activeforeground="BLACK", highlightthickness=2, highlightbackground="#05d7ff", cursor="hand2", border="1", text="UPDATE", font = ("Bahnschrift",11,"italic"), command = update_on_click, highlightcolor="white", width=25,)
    button_update.pack(padx=10, pady=50)
    button_update.place(x= 50,y=550);
    button_update.config(height= 2, width=25)
                                            #020f12                 #05d7ff
    button_add = tk.Button(frame,background="#05d7ff", foreground= "#020f12", activebackground= "#65e7ff", activeforeground="BLACK", highlightthickness=2, highlightbackground="#05d7ff", cursor="hand2", border="1", text="ADD", font = ("Bahnschrift",11,"italic"), command = add_on_click, highlightcolor="white",width=25,)
    button_add.pack(padx=10, pady=50)
    button_add.place(x= 50,y=476);
    button_add.config(height= 2, width=25)


    button_search = customtkinter.CTkButton(frame, cursor="hand2", text="Search",text_color= "black",fg_color=("white","#05d7ff"), font = ("Bahnschrift",11,"bold"), command = search_on_click, border_width=2, height= 30,width=100,corner_radius=50)
    button_search.pack()
    button_search.place(x= 186,y=435)
    
    def loggout():
        myclass.mainlogout(frame)
    logout = customtkinter.CTkButton(frame, cursor="hand2", text="Log out",text_color= "black",fg_color=("white","#05d7ff"), font = ("Bahnschrift",11,"bold"), command = loggout, border_width=2, height= 30,width=70,corner_radius=10)
    logout.pack()
    logout.place(x= 1260,y=410)

    textfield1= tk.Entry(frame, foreground= "SystemButtonFace",fg="BLACK",border=0, width=12, font=('Arial', 25,"bold italic"))
    textfield1.pack()
    
    textfield2= tk.Entry(frame, foreground= "SystemButtonFace",fg="BLACK", border=0, width=12, font=('Arial', 25,"bold italic"))
    textfield2.pack()
    
    textfield3= tk.Entry(frame, foreground= "SystemButtonFace",fg="BLACK", border=0,  width=12, font=('Arial', 25,"bold italic"))
    textfield3.pack()
    
    # search textfield
    textfield4= customtkinter.CTkEntry(frame,height=38,width=130, text_color= "black",fg_color=("blue","white") ,placeholder_text="ID search" ,font=('Arial', 18,"bold"),corner_radius=50)
    textfield4.pack()
    
    textfield5= tk.Entry(frame, foreground= "SystemButtonFace",fg="BLACK", border=0,  width=11, font=('Arial', 25,"bold italic"))
    textfield5.pack()
    
    textfield7= tk.Entry(frame, foreground= "SystemButtonFace",fg="BLACK", border=0,  width=11, font=('Arial', 25,"bold italic"))
    textfield7.pack()
    
    # Set up a custom font
    bigfont = tkFont.Font(family="Arial", size=18, weight="bold", slant="italic")
    frame.option_add("*TCombobox*Listbox*Font", bigfont)
        
    combo = ttk.Combobox(frame,values=current_username, width=13, font=("Arial", 18, "italic bold"), state="readonly")
    combo.set("-Empty-")
 
 
    switch_state = False
    def switcher():
        global switch_state
        if switch_state:
            sv_ttk.set_theme("light")
            my_switch.configure(text="LIGHT MODE  ",fg_color="grey",bg_color="white",text_color="black")
            button_add.configure(background="#05d7ff", foreground= "#020f12", activebackground= "#65e7ff", activeforeground="BLACK")
            button_update.configure(background="#05d7ff", foreground= "#020f12", activebackground= "#65e7ff", activeforeground="BLACK")
            button_delete.configure(background="#05d7ff", foreground= "#020f12", activebackground= "#65e7ff", activeforeground="BLACK")
            
            button_search.configure(cursor="hand2", text="Search",text_color= "black",fg_color=("white","#05d7ff"), font = ("Bahnschrift",11,"bold"))
            logout.configure(cursor="hand2", text="Log out",text_color= "black",fg_color=("white","#05d7ff"), font = ("Bahnschrift",11,"bold"))

            textfield4.configure(height=38,width=130, text_color= "black",fg_color=("blue","white") ,placeholder_text="ID search" ,font=('Arial', 16,"bold"),corner_radius=50)
            
            style.configure("Treeview.Heading", font=("Franklin Gothic Heavy", 14,"italic"))
            style.configure("Treeview", rowheight=80)
            style.configure("Treeview", font=("Bahnschrift", 25,"bold"))
            switch_state = False
        else:
            sv_ttk.set_theme("dark")
            my_switch.configure(text="DARK MODE  ",fg_color="blue", bg_color="#1C1C1C",text_color="white")
            button_add.configure(background="#020f12", foreground= "#020f12", activebackground= "#65e7ff", activeforeground="BLACK",fg="white")
            button_update.configure(background="#020f12", foreground= "#020f12", activebackground= "#65e7ff", activeforeground="BLACK",fg="white")
            button_delete.configure(background="#020f12", foreground= "#020f12", activebackground= "#65e7ff", activeforeground="BLACK",fg="white")
            
            button_search.configure(text_color= "white",bg_color="#1c1c1c",fg_color=("white","#020f12"))
            logout.configure(text_color= "white",bg_color="#1c1c1c",fg_color=("white","#020f12"))

            textfield4.configure(height=38,width=130, text_color= "white",bg_color="#1c1c1c",fg_color=("white","#1C1C1C") ,placeholder_text="ID search" ,font=('Arial', 16,"bold"),corner_radius=50)
            
            style.configure("Treeview.Heading", font=("Franklin Gothic Heavy", 14,"italic"))
            style.configure("Treeview", rowheight=80) 
            style.configure("Treeview", font=("Bahnschrift", 25,"bold"))
            style.map("Treeview", background=[('selected', '#cc2b5e')]) 
            
            switch_state = True
    
    my_switch = customtkinter.CTkSwitch(frame, text="DARK MODE  ", command=switcher, variable=customtkinter.StringVar(value="off"), onvalue="on",offvalue="off",font=("Bahnschrift",18,"italic"), text_color="black")
    my_switch.pack()
    my_switch.place(x=1125,y=660)

    
    textfield1_lowerLine = tk.Label(frame, text= "—————————————", bd=0, font=("Arial Black",12,"bold"),fg="#05d7ff")
    textfield1_lowerLine.pack()
    textfield1_lowerLine.place(x=513, y=508)
    
    textfield2_lowerLine = tk.Label(frame, text= "—————————————", bd=0, font=("Arial Black",12,"bold"),fg="#05d7ff")
    textfield2_lowerLine.pack()
    textfield2_lowerLine.place(x=513, y=580)
    
    textfield3_lowerLine = tk.Label(frame, text= "—————————————", bd=0, font=("Arial Black",12,"bold"),fg="#05d7ff")  
    textfield3_lowerLine.pack()
    textfield3_lowerLine.place(x=513, y=650)
    
    textfield5_lowerLine = tk.Label(frame, text= "—————————————", bd=0, font=("Arial Black",12,"bold"),fg="#05d7ff")  
    textfield5_lowerLine.pack()
    textfield5_lowerLine.place(x= 905,y=505)
    
    textfield7_lowerLine = tk.Label(frame, text= "—————————————", bd=0, font=("Arial Black",12,"bold"),fg="#05d7ff")  
    textfield7_lowerLine.pack()
    textfield7_lowerLine.place(x=905, y=574)

    
    
    textfield1.bind("<FocusIn>", lambda e: textfield1_lowerLine.config(foreground="YELLOW"))
    textfield1.bind("<FocusOut>", lambda e: textfield1_lowerLine.config(foreground="#05d7ff"))
    
    textfield2.bind("<FocusIn>", lambda e: textfield2_lowerLine.config(foreground="YELLOW"))
    textfield2.bind("<FocusOut>", lambda e: textfield2_lowerLine.config(foreground="#05d7ff"))
    
    textfield3.bind("<FocusIn>", lambda e: textfield3_lowerLine.config(foreground="YELLOW"))
    textfield3.bind("<FocusOut>", lambda e: textfield3_lowerLine.config(foreground="#05d7ff"))
    
    textfield5.bind("<FocusIn>", lambda e: textfield5_lowerLine.config(foreground="YELLOW"))
    textfield5.bind("<FocusOut>", lambda e: textfield5_lowerLine.config(foreground="#05d7ff"))
 
    textfield7.bind("<FocusIn>", lambda e: textfield7_lowerLine.config(foreground="YELLOW"))
    textfield7.bind("<FocusOut>", lambda e: textfield7_lowerLine.config(foreground="#05d7ff"))
    
    
    textfield1.place(x=513, y=469)
    textfield2.place(x=513, y=541)
    textfield3.place(x=513, y=611)
    textfield4.place(x=50, y=430)
    textfield5.place(x=910, y=460)
    textfield7.place(x=910, y=535)
    combo.place(x= 1125,y=468)

    
    text_var = tk.StringVar()
    text_var.set("Product ID:") 
    label1 = tk.Label(frame, textvariable=text_var, anchor=tk.W, font=("Franklin Gothic Heavy", 20,"italic"), justify=tk.CENTER)
    label1.pack() 
    label1.place(x= 300,y=480);

    text_var = tk.StringVar()
    text_var.set("Product Name:") 
    label2 = tk.Label(frame, textvariable=text_var, anchor=tk.W, font=("Franklin Gothic Heavy", 20,"italic"), justify=tk.CENTER)
    label2.pack() 
    label2.place(x= 300,y=550);

    text_var = tk.StringVar()
    text_var.set("Product Price:") 
    label3 = tk.Label(frame, textvariable=text_var, anchor=tk.W, font=("Franklin Gothic Heavy", 20,"italic "), justify=tk.CENTER)
    label3.pack() 
    label3.place(x= 300,y=620);
    
    text_var = tk.StringVar()
    text_var.set("Quantity:") 
    label6 = tk.Label(frame, textvariable=text_var, anchor=tk.W, font=("Franklin Gothic Heavy", 18,"italic"), justify=tk.CENTER)
    label6.pack() 
    label6.place(x= 755,y=480);
    
    text_var = tk.StringVar()
    text_var.set("Expiration:") 
    label8 = tk.Label(frame, textvariable=text_var, anchor=tk.W, font=("Franklin Gothic Heavy", 18,"italic"), justify=tk.CENTER)
    label8.pack() 
    label8.place(x= 755,y=545);

    text_var = tk.StringVar()
    text_var.set("ID Search:") 
    label4 = tk.Label(frame, textvariable=text_var, anchor=tk.W, font=("Franklin Gothic Heavy", 10,"italic"), justify=tk.CENTER)
    label4.pack() 
    label4.place(x= 50,y=405);
    
    text_var = tk.StringVar()
    text_var.set("Username: ") 
    label2 = tk.Label(frame, textvariable=text_var, anchor=tk.W, font=("Franklin Gothic Heavy", 15,"italic"), justify=tk.CENTER)
    label2.pack() 
    label2.place(x= 1125,y=436);
    
    label_var5 = tk.StringVar()
    label_var5.set("       \n         no image") 
    label5 = tk.Label(frame, textvariable=label_var5, borderwidth=4, relief="sunken", anchor=tk.W, font=("Arial", 15,"italic bold"), justify=tk.CENTER)
    label5.place(x= 1125, y=525, height= 130, width=220);

    
    tree.pack(ipady = 20)                           
    tree.place(x=10, y=30, width=1345, height=365)
    frame.mainloop()   
    
except Error as e:
        messagebox.showerror("MySQL Connection Error", f"Error connecting to MySQL: {e}")
        
finally:
    # auto delete sa textfile
     with open("username.txt", 'w') as f:
        f.write("")  
        

