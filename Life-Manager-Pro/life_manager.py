import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttb
from ttkbootstrap.constants import *
from datetime import datetime, timedelta
import json
import os
from ttkbootstrap.scrolled import ScrolledFrame
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LifeManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Life Manager Pro")
        self.root.geometry("1200x800")
        
        # Set theme
        self.style = ttb.Style(theme="cosmo")
        self.style.configure('lefttab.TNotebook', tabposition='wn')
        
        # Initialize data storage
        self.tasks = []
        self.goals = []
        self.load_data()
        
        # Initialize active page
        self.active_page = "dashboard"
        
        # Create main container with gradient background
        self.main_container = ttb.Frame(self.root, bootstyle="light")
        self.main_container.pack(fill=BOTH, expand=YES)
        
        # Create header
        self.create_header()
        
        # Create sidebar navigation
        self.create_sidebar()
        
        # Create main content area with two-panel layout
        self.content_container = ttb.Frame(self.main_container, bootstyle="light")
        self.content_container.pack(fill=BOTH, expand=YES, side=LEFT, padx=0, pady=0)
        
        # Main content area (left panel)
        self.content_frame = ttb.Frame(self.content_container, bootstyle="light")
        self.content_frame.pack(fill=BOTH, expand=YES, side=LEFT, padx=10, pady=10)
        
        # Sidebar content area (right panel)
        self.sidebar_content = ttb.Frame(self.content_container, width=300, bootstyle="light")
        self.sidebar_content.pack(fill=Y, expand=NO, side=RIGHT, padx=10, pady=10)
        self.sidebar_content.pack_propagate(False)
        
        # Initialize with dashboard
        self.show_dashboard()
        self.update_sidebar_content()

    def create_header(self):
        # Main header container with gradient effect
        header_frame = ttb.Frame(self.main_container)
        header_frame.pack(fill=X)
        
        # Create gradient effect with multiple frames
        colors = ["#1a237e", "#283593", "#303f9f", "#3949ab", "#3f51b5"]
        gradient_frame = tk.Frame(header_frame)
        gradient_frame.pack(fill=X)
        
        for i, color in enumerate(colors):
            stripe = tk.Frame(gradient_frame, height=4, bg=color)
            stripe.pack(fill=X)
            stripe.pack_propagate(False)
        
        # Main header with logo, app title and greeting
        main_header = ttb.Frame(header_frame, bootstyle="primary")
        main_header.pack(fill=X, padx=0, pady=0)
        
        # Logo and title container
        branding_frame = ttb.Frame(main_header, bootstyle="primary")
        branding_frame.pack(side=LEFT, padx=20, pady=10)
        
        # App logo (using text as logo placeholder)
        logo_label = ttb.Label(
            branding_frame,
            text="⚡",  # Unicode character as logo
            font=("Helvetica", 24, "bold"),
            bootstyle="primary inverse"
        )
        logo_label.pack(side=LEFT, padx=(0, 10))
        
        # App title with professional font
        title_label = ttb.Label(
            branding_frame,
            text="Life Manager Pro",
            font=("Helvetica", 20, "bold"),
            bootstyle="primary inverse"
        )
        title_label.pack(side=LEFT)
        
        # Right side of header with time, date and greeting
        info_frame = ttb.Frame(main_header, bootstyle="primary")
        info_frame.pack(side=RIGHT, padx=20, pady=10)
        
        # Time display
        self.time_label = ttb.Label(
            info_frame,
            text="",
            font=("Helvetica", 12, "bold"),
            bootstyle="primary inverse"
        )
        self.time_label.pack(side=RIGHT, padx=5)
        
        # Date display
        self.date_label = ttb.Label(
            info_frame,
            text=datetime.now().strftime("%A, %d %B %Y"),
            font=("Helvetica", 10),
            bootstyle="primary inverse"
        )
        self.date_label.pack(side=RIGHT, padx=5)
        

        
        # Get appropriate greeting based on time of day
        current_time = datetime.now()
        if 5 <= current_time.hour < 12:
            greeting = "Good morning"
        elif 12 <= current_time.hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        # Display greeting
 
        
        # Update time immediately (moved after creating greeting_label)
        self.update_time()

    def update_time(self):
        """Update the time display every second"""
        current_time = datetime.now().strftime("%I:%M:%S %p")
        self.time_label.config(text=current_time)
        
        # Update greeting if hour changes
        hour_now = datetime.now().hour
        if hour_now != getattr(self, 'last_hour', None):
            self.last_hour = hour_now
            self.update_greeting()
            
        self.root.after(1000, self.update_time)

    def update_greeting(self):
        """Update the greeting based on time of day"""
        current_time = datetime.now()
        if 5 <= current_time.hour < 12:
            greeting = "Good morning"
        elif 12 <= current_time.hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
   

    def create_sidebar(self):
        # Create sidebar container
        self.sidebar = ttb.Frame(self.main_container, width=200, bootstyle="secondary")
        self.sidebar.pack(fill=Y, expand=NO, side=LEFT, padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        
        # Logo and branding at top
        logo_frame = ttb.Frame(self.sidebar, bootstyle="dark")
        logo_frame.pack(fill=X, pady=0)
        
        logo_label = ttb.Label(
            logo_frame,
            text="⚡ LMP",
            font=("Helvetica", 18, "bold"),
            bootstyle="inverse"
        )
        logo_label.pack(pady=15)
        
        # Navigation menu
        nav_items = [
            ("Dashboard", "📊", self.show_dashboard),
            ("Tasks", "✓", self.show_tasks),
            ("Goals", "🎯", self.show_goals),
            ("Analytics", "📈", self.show_analytics),
            ("Settings", "⚙️", self.show_settings)
        ]
        
        for text, icon, command in nav_items:
            self.create_nav_button(text, icon, command)

    def create_nav_button(self, text, icon, command):
        btn = ttb.Button(
            self.sidebar,
            text=f"{icon} {text}",
            bootstyle="secondary-link",
            command=command,
            width=18,
            compound=LEFT
        )
        btn.pack(fill=X, padx=10, pady=3)
        return btn

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def clear_sidebar_content(self):
        for widget in self.sidebar_content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()
        self.active_page = "dashboard"
        
        # Create dashboard layout with premium styling
        dashboard = ScrolledFrame(self.content_frame, bootstyle="rounded")
        dashboard.pack(fill=BOTH, expand=YES)
        
        # Add greeting header with time-based message
        self.create_greeting_header(dashboard)
        
        # Enhanced Quick Stats with modern cards and animations
        stats_frame = ttb.Frame(dashboard)
        stats_frame.pack(fill=X, padx=20, pady=20)
        
        # Create a row for stats cards
        stats_row = ttb.Frame(stats_frame)
        stats_row.pack(fill=X)
        
        # Calculate statistics with more detailed information
        tasks_due_today = [t for t in self.tasks if self.is_due_today(t)]
        goals_in_progress = [g for g in self.goals if not g.get('completed', False)]
        completed_tasks = [t for t in self.tasks if t.get('completed', False)]
        achieved_goals = [g for g in self.goals if g.get('completed', False)]
        
        # Stats cards with different colors, icons, and hover effects
        self.create_enhanced_stat_card(stats_row, "Tasks Due Today", 
                                len(tasks_due_today), 
                                "info", "calendar-day", 
                                f"{len(tasks_due_today)} of {len(self.tasks)} total tasks")
        
        self.create_enhanced_stat_card(stats_row, "Goals in Progress", 
                                len(goals_in_progress), 
                                "success", "bullseye", 
                                f"{len(goals_in_progress)} active goals")
        
        self.create_enhanced_stat_card(stats_row, "Completed Tasks", 
                                len(completed_tasks), 
                                "primary", "check-circle", 
                                f"{(len(completed_tasks)/max(1, len(self.tasks))*100):.1f}% completion rate")
        
        self.create_enhanced_stat_card(stats_row, "Achieved Goals", 
                                len(achieved_goals), 
                                "warning", "trophy", 
                                f"{len(achieved_goals)} of {len(self.goals)} total goals")
        
        # Create second row for progress summary and charts
        dashboard_grid = ttb.Frame(dashboard)
        dashboard_grid.pack(fill=BOTH, expand=YES, padx=20, pady=10)
        
        # Create left column for dashboard
        left_column = ttb.Frame(dashboard_grid)
        left_column.pack(fill=BOTH, expand=YES)
        
        # Today's Schedule with modern card style and improved UI
        self.create_todays_schedule(left_column, tasks_due_today)
        
        # Update sidebar content
        self.update_sidebar_content()

    def create_greeting_header(self, parent):
        # Get current time and customize greeting
        current_hour = datetime.now().hour
        
        if current_hour < 12:
            greeting = "Good Morning"
        elif current_hour < 18:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"
        
        # Create greeting frame with subtle gradient background
        greeting_frame = ttb.Frame(parent, bootstyle="light")
        greeting_frame.pack(fill=X, padx=20, pady=(20, 10))
        
        # Add personalized greeting with username (if available)
        username = "User"  # Replace with actual username if you have it stored
        ttb.Label(
            greeting_frame,
            text=f"{greeting}!",
            font=("Helvetica", 18, "bold"),
            bootstyle="inverse-light"
        ).pack(side=LEFT, pady=10, padx=10)
        
        # Add date display
        current_date = datetime.now().strftime("%A, %d %B %Y")
        ttb.Label(
            greeting_frame,
            text=current_date,
            font=("Helvetica", 12),
            bootstyle="inverse-secondary"
        ).pack(side=RIGHT, pady=10, padx=10)

    def create_enhanced_stat_card(self, parent, title, value, color, icon_name, subtitle):
        # Create card frame with better styling and hover effect
        card_frame = ttb.Frame(parent, bootstyle=f"{color}")
        card_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=5)
        
        # Add animation on hover (highlight effect)
        def on_enter(e):
            card_frame.configure(bootstyle=f"{color}-strong")
            
        def on_leave(e):
            card_frame.configure(bootstyle=f"{color}")
        
        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)
        
        # Card content with icon
        content_frame = ttb.Frame(card_frame, bootstyle=f"{color}")
        content_frame.pack(fill=BOTH, expand=YES, padx=15, pady=15)
        
        # Try to load icon from ttkbootstrap icons or use text fallback
        try:
            # Use ttkbootstrap's included icons if available
            icon = ttb.PhotoImage(
                file=f"icons/{icon_name}.png",
                width=32,
                height=32
            )
            ttb.Label(
                content_frame, 
                image=icon,
                bootstyle=f"inverse-{color}"
            ).pack(side=RIGHT, padx=(10, 0))
            
            # Keep a reference to prevent garbage collection
            content_frame.icon = icon
        except:
            # Fallback to text if icon not available
            ttb.Label(
                content_frame,
                text="●",
                font=("Helvetica", 18),
                bootstyle=f"inverse-{color}"
            ).pack(side=RIGHT, padx=(10, 0))
        
        # Card value with large font
        ttb.Label(
            content_frame,
            text=str(value),
            font=("Helvetica", 24, "bold"),
            bootstyle=f"inverse-{color}"
        ).pack(anchor="w")
        
        # Card title
        ttb.Label(
            content_frame,
            text=title,
            font=("Helvetica", 10),
            bootstyle=f"inverse-{color}"
        ).pack(anchor="w")
        
        # Add subtitle with additional context
        ttb.Label(
            content_frame,
            text=subtitle,
            font=("Helvetica", 8),
            bootstyle=f"inverse-{color}"
        ).pack(anchor="w", pady=(5, 0))

    def show_tasks(self):
        self.clear_content()
        self.active_page = "tasks"
        
        # Create header with title and add button
        header_frame = ttb.Frame(self.content_frame, bootstyle="light")
        header_frame.pack(fill=X, padx=0, pady=0)
        
        # Add a gradient effect to header
        header_canvas = tk.Canvas(header_frame, height=80, highlightthickness=0)
        header_canvas.pack(fill=X)
        
        # Create gradient header
        header_canvas.create_rectangle(0, 0, 5000, 80, fill="#3498db", outline="")
        for i in range(80):
            # Create gradient from blue to slightly lighter blue
            color = f'#{37+i//8:02x}{153+i//8:02x}{220+i//8:02x}'
            header_canvas.create_line(0, i, 5000, i, fill=color)
        
        # Add title on the header
        header_canvas.create_text(30, 40, text="Task Manager", font=("Helvetica", 18, "bold"), fill="white", anchor="w")
        
        # Add search box
        search_frame = ttb.Frame(header_canvas, bootstyle="light")
        header_canvas.create_window(500, 40, window=search_frame, anchor="e")
        
        search_var = tk.StringVar()
        search_entry = ttb.Entry(search_frame, textvariable=search_var, width=20, 
                               bootstyle="light", font=("Helvetica", 11))
        search_entry.pack(side=LEFT, padx=5)
        
        # Add New Task button with icon
        add_btn = ttb.Button(
            header_canvas, 
            text="+ New Task", 
            bootstyle="success",
            command=self.add_task_dialog,
            width=15
        )
        header_canvas.create_window(30, 120, window=add_btn, anchor="w")
        
        # Main content area with scrolling
        main_content = ttb.Frame(self.content_frame)
        main_content.pack(fill=BOTH, expand=YES, padx=15, pady=(70, 15))
        
        # Create tabs for different task views
        task_tabs = ttb.Notebook(main_content)
        task_tabs.pack(fill=BOTH, expand=YES)
        
        # All tasks tab
        all_tasks_tab = ttb.Frame(task_tabs, padding=10)
        task_tabs.add(all_tasks_tab, text="All Tasks")
        
        # Today tab
        today_tab = ttb.Frame(task_tabs, padding=10)
        task_tabs.add(today_tab, text="Today")
        
        # Upcoming tab
        upcoming_tab = ttb.Frame(task_tabs, padding=10)
        task_tabs.add(upcoming_tab, text="Upcoming")
        
        # Completed tab
        completed_tab = ttb.Frame(task_tabs, padding=10)
        task_tabs.add(completed_tab, text="Completed")
        
        # Create scrollable containers for each tab
        all_container = ScrolledFrame(all_tasks_tab)
        all_container.pack(fill=BOTH, expand=YES)
        
        today_container = ScrolledFrame(today_tab)
        today_container.pack(fill=BOTH, expand=YES)
        
        upcoming_container = ScrolledFrame(upcoming_tab)
        upcoming_container.pack(fill=BOTH, expand=YES)
        
        completed_container = ScrolledFrame(completed_tab)
        completed_container.pack(fill=BOTH, expand=YES)
        
        # Set active task container
        task_container = all_container
        self.filtered_tasks = self.tasks
        
        def search_tasks(*args):
            search_term = search_var.get().lower().strip()
            current_tab = task_tabs.select()
            tab_index = task_tabs.index(current_tab)
            
            # Get the appropriate container based on current tab
            if tab_index == 0:  # All Tasks
                container = all_container
                tasks = self.tasks
            elif tab_index == 1:  # Today
                container = today_container
                today_date = datetime.now().strftime('%Y-%m-%d')
                tasks = [t for t in self.tasks if t.get('date') == today_date]
            elif tab_index == 2:  # Upcoming
                container = upcoming_container
                today_date = datetime.now().strftime('%Y-%m-%d')
                tasks = [t for t in self.tasks if t.get('date') > today_date]
            else:  # Completed
                container = completed_container
                tasks = [t for t in self.tasks if t.get('completed', False)]
            
            # Filter tasks based on search term
            if search_term:
                self.filtered_tasks = [
                    t for t in tasks 
                    if search_term in t.get('title', '').lower() or 
                       search_term in t.get('description', '').lower()
                ]
            else:
                self.filtered_tasks = tasks
            
            # Render the filtered tasks
            self.render_task_list(container)
        
        # Bind search function to search box
        search_var.trace_add('write', search_tasks)
        
        # Add search button
        search_btn = ttb.Button(
            search_frame,
            text="🔍",
            command=search_tasks,
            bootstyle="light-outline",
            width=3
        )
        search_btn.pack(side=LEFT)
        
        # Handle tab changes
        def tab_changed(event):
            nonlocal task_container
            tab_index = task_tabs.index(task_tabs.select())
            
            if tab_index == 0:  # All Tasks
                task_container = all_container
                self.filtered_tasks = self.tasks
            elif tab_index == 1:  # Today
                task_container = today_container
                today_date = datetime.now().strftime('%Y-%m-%d')
                self.filtered_tasks = [t for t in self.tasks if t.get('date') == today_date]
            elif tab_index == 2:  # Upcoming
                task_container = upcoming_container
                today_date = datetime.now().strftime('%Y-%m-%d')
                self.filtered_tasks = [t for t in self.tasks if t.get('date') > today_date]
            elif tab_index == 3:  # Completed
                task_container = completed_container
                self.filtered_tasks = [t for t in self.tasks if t.get('completed', False)]
            
            # Re-apply search filter if there's a search term
            search_tasks()
        
        task_tabs.bind("<<NotebookTabChanged>>", tab_changed)
        
        # Initial render
        self.render_task_list(task_container)
        
        # Right sidebar panel
        right_panel = ttb.Frame(self.content_frame, width=300)
        right_panel.pack(fill=Y, expand=NO, side=RIGHT)
        right_panel.pack_propagate(False)
        
        # Quick Actions
        actions_frame = ttb.Labelframe(right_panel, text="Quick Actions", padding=10)
        actions_frame.pack(fill=X, padx=5, pady=5)
        
        ttb.Button(
            actions_frame,
            text="+ New Task",
            command=self.add_task_dialog,
            bootstyle="success-outline",
            width=20
        ).pack(pady=2)
        
        # Recent Activity
        activity_frame = ttb.Labelframe(right_panel, text="Recent Activity", padding=10)
        activity_frame.pack(fill=X, padx=5, pady=5)
        
        # Example activities
        activities = [
            ("Added new task", "5 mins ago"),
            ("Completed goal", "1 hour ago"),
            ("Updated task", "2 hours ago")
        ]
        
        for activity, time in activities:
            activity_item = ttb.Frame(activity_frame)
            activity_item.pack(fill=X, pady=2)
            
            ttb.Label(
                activity_item,
                text=activity,
                font=("Helvetica", 10),
                bootstyle="primary"
            ).pack(side=LEFT)
            
            ttb.Label(
                activity_item,
                text=time,
                font=("Helvetica", 8),
                bootstyle="secondary"
            ).pack(side=RIGHT)

    def add_task_dialog(self):
        dialog = ttb.Toplevel(self.root)
        dialog.title("Add New Task")
        dialog.geometry("400x500")
        
        form_frame = ttb.Frame(dialog, padding=20)
        form_frame.pack(fill=BOTH, expand=YES)
        
        # Task title
        ttb.Label(form_frame, text="Task Title:").pack(anchor=W, pady=(0, 5))
        title_var = tk.StringVar()
        ttb.Entry(form_frame, textvariable=title_var).pack(fill=X, pady=(0, 10))
        
        # Date
        ttb.Label(form_frame, text="Date:").pack(anchor=W, pady=(0, 5))
        date_entry = ttb.DateEntry(form_frame, firstweekday=0, dateformat="%Y-%m-%d")
        date_entry.pack(fill=X, pady=(0, 10))
        
        # Time
        ttb.Label(form_frame, text="Time:").pack(anchor=W, pady=(0, 5))
        time_frame = ttb.Frame(form_frame)
        time_frame.pack(fill=X, pady=(0, 10))
        
        def validate_spinbox(value):
            if not value:
                return True
            try:
                val = int(value)
                return True
            except ValueError:
                return False
        
        validate_cmd = (dialog.register(validate_spinbox), '%P')
        
        hours = ttb.Spinbox(
            time_frame,
            from_=0,
            to=23,
            width=5,
            format="%02.0f",
            validate="key",
            validatecommand=validate_cmd
        )
        hours.pack(side=LEFT)
        
        ttb.Label(time_frame, text=":").pack(side=LEFT, padx=2)
        
        minutes = ttb.Spinbox(
            time_frame,
            from_=0,
            to=59,
            width=5,
            format="%02.0f",
            validate="key",
            validatecommand=validate_cmd
        )
        minutes.pack(side=LEFT)
        
        # Set default time
        current_time = datetime.now()
        hours.set(f"{current_time.hour:02d}")
        minutes.set(f"{current_time.minute:02d}")
        
        # Priority
        ttb.Label(form_frame, text="Priority:").pack(anchor=W, pady=(0, 5))
        priority_var = tk.StringVar(value="Medium")
        ttb.Combobox(
            form_frame,
            textvariable=priority_var,
            values=["Low", "Medium", "High"],
            state="readonly"
        ).pack(fill=X, pady=(0, 10))
        
        # Description
        ttb.Label(form_frame, text="Description:").pack(anchor=W, pady=(0, 5))
        description_text = tk.Text(form_frame, height=4)
        description_text.pack(fill=X, pady=(0, 10))
        
        def save_task():
            try:
                # Validate inputs
                if not title_var.get().strip():
                    raise ValueError("Task title is required")
                
                # Get and validate time
                try:
                    hour = int(hours.get())
                    minute = int(minutes.get())
                    if not (0 <= hour <= 23 and 0 <= minute <= 59):
                        raise ValueError
                    task_time = f"{hour:02d}:{minute:02d}"
                except ValueError:
                    raise ValueError("Invalid time format")
                
                # Get the date
                selected_date = date_entry.entry.get()
                if not selected_date:
                    raise ValueError("Date is required")
                
                # Validate date format
                try:
                    datetime.strptime(selected_date, "%Y-%m-%d")
                except ValueError:
                    raise ValueError("Invalid date format")
                
                task = {
                    'title': title_var.get().strip(),
                    'date': selected_date,
                    'time': task_time,
                    'priority': priority_var.get(),
                    'description': description_text.get("1.0", tk.END).strip(),
                    'completed': False
                }
                
                self.tasks.append(task)
                self.save_data()
                dialog.destroy()
                self.show_tasks()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save task: {str(e)}")
        
        ttb.Button(
            form_frame,
            text="Save Task",
            command=save_task,
            bootstyle="success"
        ).pack(pady=20)

    def show_goals(self):
        self.clear_content()
        self.active_page = "goals"
        
        # Create goals layout
        goals_frame = ScrolledFrame(self.content_frame)
        goals_frame.pack(fill=BOTH, expand=YES)
        
        # Add goal button
        add_frame = ttb.Frame(goals_frame)
        add_frame.pack(fill=X, padx=20, pady=10)
        
        ttb.Button(
            add_frame,
            text="Add New Goal",
            command=self.add_goal_dialog,
            style="success.TButton",
            width=20
        ).pack(side=LEFT)
        
        # Goals list
        goals_list = ttb.Labelframe(goals_frame, text="Your Goals", padding=10)
        goals_list.pack(fill=X, padx=20, pady=10)
        
        if not self.goals:
            ttb.Label(
                goals_list,
                text="No goals added yet",
                bootstyle="secondary"
            ).pack(pady=10)
        else:
            for goal in self.goals:
                self.create_goal_item(goals_list, goal)
        
        # Right sidebar panel
        right_panel = ttb.Frame(self.content_frame, width=300)
        right_panel.pack(fill=Y, expand=NO, side=RIGHT)
        right_panel.pack_propagate(False)
        
        # Goal Statistics
        stats_frame = ttb.Labelframe(right_panel, text="Goal Statistics", padding=10)
        stats_frame.pack(fill=X, padx=5, pady=5)
        
        stats = [
            ("Total Goals", len(self.goals)),
            ("In Progress", len([g for g in self.goals if not g.get('completed', False)])),
            ("Achieved", len([g for g in self.goals if g.get('completed', False)]))
        ]
        
        for label, value in stats:
            stat_item = ttb.Frame(stats_frame)
            stat_item.pack(fill=X, pady=2)
            
            ttb.Label(
                stat_item,
                text=label,
                font=("Helvetica", 10),
                bootstyle="secondary"
            ).pack(side=LEFT)
            
            ttb.Label(
                stat_item,
                text=str(value),
                font=("Helvetica", 10, "bold"),
                bootstyle="primary"
            ).pack(side=RIGHT)
        
        # Categories
        categories_frame = ttb.Labelframe(right_panel, text="Categories", padding=10)
        categories_frame.pack(fill=X, padx=5, pady=5)
        
        categories = self.get_goal_categories()
        
        for category, count in categories.items():
            category_item = ttb.Frame(categories_frame)
            category_item.pack(fill=X, pady=2)
            
            ttb.Label(
                category_item,
                text=category,
                font=("Helvetica", 10),
                bootstyle="secondary"
            ).pack(side=LEFT)
            
            ttb.Label(
                category_item,
                text=str(count),
                font=("Helvetica", 10, "bold"),
                bootstyle="primary"
            ).pack(side=RIGHT)

    def add_goal_dialog(self):
        dialog = ttb.Toplevel(self.root)
        dialog.title("Add New Goal")
        dialog.geometry("400x600")
        
        form_frame = ttb.Frame(dialog, padding=20)
        form_frame.pack(fill=BOTH, expand=YES)
        
        # Goal title
        ttb.Label(form_frame, text="Goal Title:").pack(anchor=W, pady=(0, 5))
        title_var = tk.StringVar()
        ttb.Entry(form_frame, textvariable=title_var).pack(fill=X, pady=(0, 10))
        
        # Target date
        ttb.Label(form_frame, text="Target Date:").pack(anchor=W, pady=(0, 5))
        date_entry = ttb.DateEntry(form_frame, firstweekday=0)
        date_entry.pack(fill=X, pady=(0, 10))
        
        # Set default date to 30 days from now
        future_date = datetime.now() + timedelta(days=30)
        date_entry.entry.delete(0, tk.END)
        date_entry.entry.insert(0, future_date.strftime("%Y-%m-%d"))
        
        # Category
        ttb.Label(form_frame, text="Category:").pack(anchor=W, pady=(0, 5))
        category_var = tk.StringVar(value="Personal")
        ttb.Combobox(
            form_frame,
            textvariable=category_var,
            values=["Personal", "Professional", "Health", "Financial", "Educational"],
            state="readonly"
        ).pack(fill=X, pady=(0, 10))
        
        # Description
        ttb.Label(form_frame, text="Description:").pack(anchor=W, pady=(0, 5))
        description_text = tk.Text(form_frame, height=4)
        description_text.pack(fill=X, pady=(0, 10))
        
        # Milestones
        ttb.Label(form_frame, text="Milestones:").pack(anchor=W, pady=(0, 5))
        milestones_text = tk.Text(form_frame, height=4)
        milestones_text.pack(fill=X, pady=(0, 10))
        
        def save_goal():
            try:
                goal = {
                    'title': title_var.get(),
                    'target_date': date_entry.entry.get(),
                    'category': category_var.get(),
                    'description': description_text.get("1.0", tk.END).strip(),
                    'milestones': [m for m in milestones_text.get("1.0", tk.END).strip().split('\n') if m],
                    'completed': False
                }
                
                self.goals.append(goal)
                self.save_data()
                dialog.destroy()
                self.show_goals()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save goal: {str(e)}")
        
        ttb.Button(
            form_frame,
            text="Save Goal",
            command=save_goal,
            style="success.TButton"
        ).pack(pady=20)

    def show_calendar(self):
        self.clear_content()
        
        # Create calendar layout
        calendar_frame = ttb.Frame(self.content_frame)
        calendar_frame.pack(fill=BOTH, expand=YES)
        
        # Calendar header
        header_frame = ttb.Frame(calendar_frame)
        header_frame.pack(fill=X, padx=20, pady=10)
        
        current_date = datetime.now()
        month_year = current_date.strftime("%B %Y")
        
        ttb.Label(
            header_frame,
            text=month_year,
            font=("Helvetica", 16, "bold")
        ).pack(side=LEFT)
        
        # Calendar grid
        grid_frame = ttb.Frame(calendar_frame)
        grid_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)
        
        # Days of week header
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            ttb.Label(
                grid_frame,
                text=day,
                font=("Helvetica", 10, "bold")
            ).grid(row=0, column=i, pady=5)

    def create_task_item(self, parent, task):
        # Determine task priority and set appropriate styling
        priority = task.get('priority', 'Medium')
        completed = task.get('completed', False)
        
        # Set color based on priority and completion status
        if completed:
            border_color = "#888888"
            background_color = "#f0f0f0"
        elif priority == "High":
            border_color = "#e74c3c"
            background_color = "#fdedec"
        elif priority == "Medium":
            border_color = "#f39c12"
            background_color = "#fef5e7"
        else:  # Low
            border_color = "#3498db"
            background_color = "#ebf5fb"
        
        # Create task frame with custom styling
        task_frame = ttb.Frame(parent, height=90, relief="solid", borderwidth=1)
        task_frame.pack(fill=X, padx=10, pady=5)
        task_frame.pack_propagate(False)  # Maintain fixed height
        
        # Add a canvas for the left border color indicator
        indicator = tk.Canvas(task_frame, width=4, highlightthickness=0)
        indicator.pack(side=LEFT, fill=Y)
        indicator.create_rectangle(0, 0, 10, 500, fill=border_color, outline="")
        
        # Create content frame
        content = ttb.Frame(task_frame, padding=10)
        content.pack(side=LEFT, fill=BOTH, expand=YES)
        
        # Title with strikethrough if completed
        title_text = task.get('title', 'Untitled Task')
        if completed:
            title_text = "✓ " + title_text
        
        title = ttb.Label(
            content,
            text=title_text,
            font=("Helvetica", 12, "bold"),
            anchor="w",
            bootstyle="secondary" if completed else "default"
        )
        title.pack(anchor=W, pady=(0, 5))
        
        # Description (if available)
        description = task.get('description', '').strip()
        if description:
            desc_label = ttb.Label(
                content,
                text=description[:75] + ('...' if len(description) > 75 else ''),
                bootstyle="secondary",
                anchor="w"
            )
            desc_label.pack(anchor=W, fill=X)
        
        # Time and additional info at bottom
        info_frame = ttb.Frame(content)
        info_frame.pack(fill=X, pady=(5, 0), anchor=W)
        
        # Format time nicely
        time_str = task.get('time', '')
        if time_str:
            try:
                time_obj = datetime.strptime(time_str, '%H:%M')
                time_str = time_obj.strftime('%I:%M %p')
            except ValueError:
                pass
        
        # Add time label
        time_label = ttb.Label(
            info_frame,
            text=time_str,
            bootstyle="secondary",
            font=("Helvetica", 10)
        )
        time_label.pack(side=LEFT)
        
        # Add priority indicator
        if not completed:
            priority_text = f"• {priority} Priority"
            priority_label = ttb.Label(
                info_frame,
                text=priority_text,
                bootstyle="secondary",
                font=("Helvetica", 10)
            )
            priority_label.pack(side=LEFT, padx=(10, 0))
        
        # Button frame on the right
        btn_frame = ttb.Frame(task_frame)
        btn_frame.pack(side=RIGHT, padx=10, fill=Y)
        
        # Add action buttons
        if not completed:
            complete_btn = ttb.Button(
                btn_frame,
                text="Complete",
                bootstyle="success-outline",
                command=lambda: self.complete_task(task),
                width=9
            )
            complete_btn.pack(side=TOP, pady=5)
        
        delete_btn = ttb.Button(
            btn_frame,
            text="Delete",
            bootstyle="danger-outline",
            command=lambda: self.delete_task(task),
            width=9
        )
        delete_btn.pack(side=TOP, pady=5)
        
        # Make entire task clickable for details
        for widget in [task_frame, content, title, info_frame]:
            widget.bind("<Button-1>", lambda e, t=task: self.show_task_details(t))
            widget.bind("<Enter>", lambda e, tf=task_frame: self.on_task_hover(tf, True))
            widget.bind("<Leave>", lambda e, tf=task_frame: self.on_task_hover(tf, False))

    def create_goal_item(self, parent, goal):
        goal_frame = ttb.Frame(parent, bootstyle="light")
        goal_frame.pack(fill=X, pady=5)
        
        # Goal card
        card = ttb.Frame(goal_frame, bootstyle="light")
        card.pack(fill=X, padx=5, pady=2)
        
        # Goal content
        content_frame = ttb.Frame(card)
        content_frame.pack(fill=X, padx=10, pady=5)
        
        # Title and category in one row
        header_frame = ttb.Frame(content_frame)
        header_frame.pack(fill=X)
        
        ttb.Label(
            header_frame,
            text=goal['title'],
            font=("Helvetica", 12, "bold")
        ).pack(side=LEFT)
        
        ttb.Label(
            header_frame,
            text=goal['category'],
            bootstyle="info"
        ).pack(side=LEFT, padx=5)
        
        ttb.Label(
            header_frame,
            text=f"Due: {goal['target_date']}",
            bootstyle="secondary"
        ).pack(side=RIGHT)
        
        if goal.get('description'):
            ttb.Label(
                content_frame,
                text=goal['description'],
                font=("Helvetica", 10),
                bootstyle="secondary",
                wraplength=600
            ).pack(anchor=W, pady=(5, 0))
        
        # Milestones
        if goal.get('milestones'):
            milestone_frame = ttb.Frame(content_frame)
            milestone_frame.pack(fill=X, pady=(5, 0))
            
            ttb.Label(
                milestone_frame,
                text="Milestones:",
                font=("Helvetica", 10, "bold"),
                bootstyle="secondary"
            ).pack(anchor=W)
            
            for milestone in goal['milestones']:
                ttb.Label(
                    milestone_frame,
                    text=f"• {milestone}",
                    font=("Helvetica", 10),
                    bootstyle="secondary",
                    wraplength=600
                ).pack(anchor=W)
        
        # Action buttons
        button_frame = ttb.Frame(content_frame)
        button_frame.pack(fill=X, pady=(5, 0))
        
        # Delete button
        ttb.Button(
            button_frame,
            text="Delete",
            command=lambda g=goal: self.delete_goal(g),
            bootstyle="danger-outline",
            width=8
        ).pack(side=RIGHT, padx=5)
        
        if goal.get('completed', False):
            ttb.Label(
                button_frame,
                text="✓ Achieved",
                font=("Helvetica", 10),
                bootstyle="success"
            ).pack(side=RIGHT)
        else:
            ttb.Button(
                button_frame,
                text="Mark Achieved",
                command=lambda g=goal: self.complete_goal(g),
                bootstyle="success-outline",
                width=12
            ).pack(side=RIGHT, padx=5)

    def delete_task(self, task):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            try:
                self.tasks.remove(task)
                self.save_data()
                self.show_tasks()
                messagebox.showinfo("Success", "Task deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete task: {str(e)}")

    def delete_goal(self, goal):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this goal?"):
            try:
                self.goals.remove(goal)
                self.save_data()
                self.show_goals()
                messagebox.showinfo("Success", "Goal deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete goal: {str(e)}")

    def complete_task(self, task):
        task['completed'] = True
        self.save_data()
        self.show_tasks()

    def complete_goal(self, goal):
        goal['completed'] = True
        self.save_data()
        self.show_goals()

    def is_due_today(self, task):
        return task['date'] == datetime.now().strftime("%Y-%m-%d")

    def load_data(self):
        try:
            if os.path.exists('life_manager_data.json'):
                with open('life_manager_data.json', 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                    self.goals = data.get('goals', [])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def save_data(self):
        try:
            with open('life_manager_data.json', 'w') as f:
                json.dump({
                    'tasks': self.tasks,
                    'goals': self.goals
                }, f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")

   

    def update_sidebar_content(self):
        self.clear_sidebar_content()
        
        # Show different content based on active page
        if self.active_page == "dashboard":
            self.show_dashboard_sidebar()
        elif self.active_page == "tasks":
            self.show_tasks_sidebar()
        elif self.active_page == "goals":
            self.show_goals_sidebar()
        elif self.active_page == "analytics":
            self.show_analytics_sidebar()
        elif self.active_page == "settings":
            self.show_settings_sidebar()

    def show_dashboard_sidebar(self):
        # Quick Actions
        actions_frame = ttb.Labelframe(self.sidebar_content, text="Quick Actions", padding=10)
        actions_frame.pack(fill=X, padx=5, pady=5)
        
        ttb.Button(
            actions_frame,
            text="+ New Task",
            command=self.add_task_dialog,
            bootstyle="success-outline",
            width=20
        ).pack(pady=2)
        
        ttb.Button(
            actions_frame,
            text="+ New Goal",
            command=self.add_goal_dialog,
            bootstyle="primary-outline",
            width=20
        ).pack(pady=2)
        
        # Recent Activity
        activity_frame = ttb.Labelframe(self.sidebar_content, text="Recent Activity", padding=10)
        activity_frame.pack(fill=X, padx=5, pady=5)
        
        # Example activities
        activities = [
            ("Added new task", "5 mins ago"),
            ("Completed goal", "1 hour ago"),
            ("Updated task", "2 hours ago")
        ]
        
        for activity, time in activities:
            activity_item = ttb.Frame(activity_frame)
            activity_item.pack(fill=X, pady=2)
            
            ttb.Label(
                activity_item,
                text=activity,
                font=("Helvetica", 10),
                bootstyle="primary"
            ).pack(side=LEFT)
            
            ttb.Label(
                activity_item,
                text=time,
                font=("Helvetica", 8),
                bootstyle="secondary"
            ).pack(side=RIGHT)

        # Add Goal Progress section below Recent Activity
        goals_in_progress = [g for g in self.goals if not g.get('completed', False)]
        achieved_goals = [g for g in self.goals if g.get('completed', False)]
        
        goals_frame = ttb.Labelframe(self.sidebar_content, text="Goal Progress", padding=10)
        goals_frame.pack(fill=X, padx=5, pady=5)
        
        if not goals_in_progress and not achieved_goals:
            ttb.Label(
                goals_frame,
                text="No goals set yet",
                font=("Helvetica", 10),
                bootstyle="secondary"
            ).pack(pady=5)
            
            ttb.Button(
                goals_frame,
                text="+ Set New Goal",
                command=self.add_goal_dialog,
                bootstyle="success-outline",
                width=15
            ).pack(pady=5)
        else:
            # Show in-progress goals
            for goal in goals_in_progress:
                goal_item = ttb.Frame(goals_frame)
                goal_item.pack(fill=X, pady=2)
                
                # Goal title and progress
                title_frame = ttb.Frame(goal_item)
                title_frame.pack(fill=X)
                
                ttb.Label(
                    title_frame,
                    text=goal.get('title', 'Untitled Goal'),
                    font=("Helvetica", 10),
                    bootstyle="primary"
                ).pack(side=LEFT)
                
                ttb.Label(
                    title_frame,
                    text=f"{goal.get('progress', 0)}%",
                    font=("Helvetica", 8),
                    bootstyle="success"
                ).pack(side=RIGHT)
                
                # Progress bar
                progress_bar = ttb.Progressbar(
                    goal_item,
                    value=goal.get('progress', 0),
                    bootstyle="success-striped"
                )
                progress_bar.pack(fill=X, pady=(2, 5))
                
                # Target date and update button in one row
                bottom_frame = ttb.Frame(goal_item)
                bottom_frame.pack(fill=X)
                
                ttb.Label(
                    bottom_frame,
                    text=f"Target: {goal.get('target_date', 'No date')}",
                    font=("Helvetica", 8),
                    bootstyle="secondary"
                ).pack(side=LEFT)
                
                ttb.Button(
                    bottom_frame,
                    text="Update",
                    command=lambda g=goal: self.update_goal_progress(g),
                    bootstyle="success-link",
                    width=8
                ).pack(side=RIGHT)

    def show_tasks_sidebar(self):
        # Task Statistics
        stats_frame = ttb.Labelframe(self.sidebar_content, text="Task Statistics", padding=10)
        stats_frame.pack(fill=X, padx=5, pady=5)
        
        stats = [
            ("Total Tasks", len(self.tasks)),
            ("Completed", len([t for t in self.tasks if t.get('completed', False)])),
            ("Due Today", len([t for t in self.tasks if self.is_due_today(t)])),
            ("Overdue", len([t for t in self.tasks if self.is_overdue(t)]))
        ]
        
        for label, value in stats:
            stat_item = ttb.Frame(stats_frame)
            stat_item.pack(fill=X, pady=2)
            
            ttb.Label(
                stat_item,
                text=label,
                font=("Helvetica", 10),
                bootstyle="secondary"
            ).pack(side=LEFT)
            
            ttb.Label(
                stat_item,
                text=str(value),
                font=("Helvetica", 10, "bold"),
                bootstyle="primary"
            ).pack(side=RIGHT)
        
        # Quick Filters
        filters_frame = ttb.Labelframe(self.sidebar_content, text="Quick Filters", padding=10)
        filters_frame.pack(fill=X, padx=5, pady=5)
        
        filters = [
            ("All Tasks", lambda: self.filter_tasks("all")),
            ("Due Today", lambda: self.filter_tasks("today")),
            ("Upcoming", lambda: self.filter_tasks("upcoming")),
            ("Completed", lambda: self.filter_tasks("completed"))
        ]
        
        for text, command in filters:
            ttb.Button(
                filters_frame,
                text=text,
                command=command,
                bootstyle="secondary-outline",
                width=20
            ).pack(pady=2)

    def show_goals_sidebar(self):
        # Goal Statistics
        stats_frame = ttb.Labelframe(self.sidebar_content, text="Goal Statistics", padding=10)
        stats_frame.pack(fill=X, padx=5, pady=5)
        
        stats = [
            ("Total Goals", len(self.goals)),
            ("In Progress", len([g for g in self.goals if not g.get('completed', False)])),
            ("Achieved", len([g for g in self.goals if g.get('completed', False)]))
        ]
        
        for label, value in stats:
            stat_item = ttb.Frame(stats_frame)
            stat_item.pack(fill=X, pady=2)
            
            ttb.Label(
                stat_item,
                text=label,
                font=("Helvetica", 10),
                bootstyle="secondary"
            ).pack(side=LEFT)
            
            ttb.Label(
                stat_item,
                text=str(value),
                font=("Helvetica", 10, "bold"),
                bootstyle="primary"
            ).pack(side=RIGHT)
        
        # Categories
        categories_frame = ttb.Labelframe(self.sidebar_content, text="Categories", padding=10)
        categories_frame.pack(fill=X, padx=5, pady=5)
        
        categories = self.get_goal_categories()
        
        for category, count in categories.items():
            category_item = ttb.Frame(categories_frame)
            category_item.pack(fill=X, pady=2)
            
            ttb.Label(
                category_item,
                text=category,
                font=("Helvetica", 10),
                bootstyle="secondary"
            ).pack(side=LEFT)
            
            ttb.Label(
                category_item,
                text=str(count),
                font=("Helvetica", 10, "bold"),
                bootstyle="primary"
            ).pack(side=RIGHT)

    def show_calendar_sidebar(self):
        # Mini Calendar
        calendar_frame = ttb.Labelframe(self.sidebar_content, text="Calendar", padding=10)
        calendar_frame.pack(fill=X, padx=5, pady=5)
        
        # Current month and year
        current_date = datetime.now()
        month_year = current_date.strftime("%B %Y")
        
        header_frame = ttb.Frame(calendar_frame)
        header_frame.pack(fill=X, pady=5)
        
        ttb.Label(
            header_frame,
            text=month_year,
            font=("Helvetica", 10, "bold"),
            bootstyle="primary"
        ).pack()
        
        # Calendar grid
        cal = calendar.monthcalendar(current_date.year, current_date.month)
        
        # Days of week header
        days_frame = ttb.Frame(calendar_frame)
        days_frame.pack(fill=X)
        
        for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            ttb.Label(
                days_frame,
                text=day,
                font=("Helvetica", 8),
                bootstyle="secondary",
                width=3
            ).pack(side=LEFT, padx=1)
        
        # Calendar days
        for week in cal:
            week_frame = ttb.Frame(calendar_frame)
            week_frame.pack(fill=X)
            
            for day in week:
                if day == 0:
                    # Empty day
                    ttb.Label(
                        week_frame,
                        text="",
                        width=3
                    ).pack(side=LEFT, padx=1, pady=1)
                else:
                    # Regular day
                    style = "primary" if day == current_date.day else "secondary"
                    ttb.Label(
                        week_frame,
                        text=str(day),
                        font=("Helvetica", 8),
                        bootstyle=style,
                        width=3
                    ).pack(side=LEFT, padx=1, pady=1)

    def show_analytics_sidebar(self):
        # Summary Statistics
        stats_frame = ttb.Labelframe(self.sidebar_content, text="Summary", padding=10)
        stats_frame.pack(fill=X, padx=5, pady=5)
        
        stats = [
            ("Task Completion Rate", f"{self.calculate_completion_rate()}%"),
            ("Active Goals", len([g for g in self.goals if not g.get('completed', False)])),
            ("Tasks This Week", len([t for t in self.tasks if self.is_this_week(t)]))
        ]
        
        for label, value in stats:
            stat_item = ttb.Frame(stats_frame)
            stat_item.pack(fill=X, pady=2)
            
            ttb.Label(
                stat_item,
                text=label,
                font=("Helvetica", 10),
                bootstyle="secondary"
            ).pack(side=LEFT)
            
            ttb.Label(
                stat_item,
                text=str(value),
                font=("Helvetica", 10, "bold"),
                bootstyle="primary"
            ).pack(side=RIGHT)
        
        # Export Options
        export_frame = ttb.Labelframe(self.sidebar_content, text="Export", padding=10)
        export_frame.pack(fill=X, padx=5, pady=5)
        
        ttb.Button(
            export_frame,
            text="Export as PDF",
            command=self.export_analytics,
            bootstyle="info-outline",
            width=20
        ).pack(pady=2)
        
        ttb.Button(
            export_frame,
            text="Export as CSV",
            command=self.export_analytics,
            bootstyle="info-outline",
            width=20
        ).pack(pady=2)

    def show_settings_sidebar(self):
        # App Info
        info_frame = ttb.Labelframe(self.sidebar_content, text="App Info", padding=10)
        info_frame.pack(fill=X, padx=5, pady=5)
        
        info = [
            ("Version", "1.2.0"),
            ("Last Update", "2024-02-20"),
            ("Storage Used", "2.3 MB")
        ]
        
        for label, value in info:
            info_item = ttb.Frame(info_frame)
            info_item.pack(fill=X, pady=2)
            
            ttb.Label(
                info_item,
                text=label,
                font=("Helvetica", 10),
                bootstyle="secondary"
            ).pack(side=LEFT)
            
            ttb.Label(
                info_item,
                text=value,
                font=("Helvetica", 10, "bold"),
                bootstyle="primary"
            ).pack(side=RIGHT)
        
        # Quick Actions
        actions_frame = ttb.Labelframe(self.sidebar_content, text="Quick Actions", padding=10)
        actions_frame.pack(fill=X, padx=5, pady=5)
        
        ttb.Button(
            actions_frame,
            text="Backup Data",
            command=self.backup_data,
            bootstyle="warning-outline",
            width=20
        ).pack(pady=2)
        
        ttb.Button(
            actions_frame,
            text="Clear All Data",
            command=self.clear_all_data,
            bootstyle="danger-outline",
            width=20
        ).pack(pady=2)

    def get_goal_categories(self):
        categories = {}
        for goal in self.goals:
            category = goal.get('category', 'Uncategorized')
            categories[category] = categories.get(category, 0) + 1
        return categories

    def calculate_completion_rate(self):
        completed = len([t for t in self.tasks if t.get('completed', False)])
        total = len(self.tasks)
        return round((completed / total * 100) if total > 0 else 0)

    def is_this_week(self, task):
        try:
            task_date = datetime.strptime(task['date'], "%Y-%m-%d").date()
            today = datetime.now().date()
            monday = today - timedelta(days=today.weekday())
            return monday <= task_date <= monday + timedelta(days=6)
        except:
            return False

    def export_analytics(self):
        messagebox.showinfo("Export", "Analytics export feature coming soon!")

    def backup_data(self):
        try:
            backup_data = {
                'tasks': self.tasks,
                'goals': self.goals
            }
            
            backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f)
            
            messagebox.showinfo("Success", f"Data backed up successfully to {backup_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to backup data: {str(e)}")

    def clear_all_data(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all data? This action cannot be undone."):
            try:
                self.tasks = []
                self.goals = []
                self.save_data()
                messagebox.showinfo("Success", "All data cleared successfully!")
                self.show_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear data: {str(e)}")

    def show_analytics(self):
        self.clear_content()
        self.active_page = "analytics"
        
        # Create analytics layout
        analytics_frame = ScrolledFrame(self.content_frame, bootstyle="rounded")
        analytics_frame.pack(fill=BOTH, expand=YES)
        
        # Header
        header_frame = ttb.Frame(analytics_frame)
        header_frame.pack(fill=X, padx=20, pady=10)
        
        ttb.Label(
            header_frame,
            text="Analytics",
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        ).pack(side=LEFT)
        
        # Task Completion Trends
        trends_frame = ttb.Labelframe(analytics_frame, text="Task Completion Trends", padding=15)
        trends_frame.pack(fill=X, padx=20, pady=10)
        
        # Create a figure for the plot
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Example data - replace with actual data
        dates = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        completed = [5, 3, 7, 4, 6, 2, 4]
        total = [8, 5, 8, 6, 8, 4, 5]
        
        # Plot bars
        x = range(len(dates))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], completed, width, label='Completed', color='#28a745')
        ax.bar([i + width/2 for i in x], total, width, label='Total', color='#007bff')
        
        ax.set_xticks(x)
        ax.set_xticklabels(dates)
        ax.legend()
        ax.set_title('Weekly Task Overview')
        
        # Embed the plot
        canvas = FigureCanvasTkAgg(fig, master=trends_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)
        
        # Goal Progress
        goals_frame = ttb.Labelframe(analytics_frame, text="Goal Progress", padding=15)
        goals_frame.pack(fill=X, padx=20, pady=10)
        
        # Create pie chart for goal categories
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        
        # Example data - replace with actual data
        categories = ['Personal', 'Professional', 'Health', 'Financial']
        sizes = [15, 30, 25, 30]
        colors = ['#007bff', '#28a745', '#ffc107', '#dc3545']
        
        ax2.pie(sizes, labels=categories, colors=colors, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        
        # Embed the plot
        canvas2 = FigureCanvasTkAgg(fig2, master=goals_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=YES)
        
        # Update sidebar
        self.update_sidebar_content()

    def show_settings(self):
        self.clear_content()
        self.active_page = "settings"
        
        # Create settings layout
        settings_frame = ScrolledFrame(self.content_frame, bootstyle="rounded")
        settings_frame.pack(fill=BOTH, expand=YES)
        
        # Header
        header_frame = ttb.Frame(settings_frame)
        header_frame.pack(fill=X, padx=20, pady=10)
        
        ttb.Label(
            header_frame,
            text="Settings",
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        ).pack(side=LEFT)
        
        # General Settings
        general_frame = ttb.Labelframe(settings_frame, text="General Settings", padding=15)
        general_frame.pack(fill=X, padx=20, pady=10)
        
        # Theme selection
        theme_frame = ttb.Frame(general_frame)
        theme_frame.pack(fill=X, pady=5)
        
        ttb.Label(
            theme_frame,
            text="Theme:",
            font=("Helvetica", 10, "bold")
        ).pack(side=LEFT)
        
        theme_var = tk.StringVar(value="cosmo")
        theme_combo = ttb.Combobox(
            theme_frame,
            textvariable=theme_var,
            values=["cosmo", "darkly", "litera", "lumen", "pulse", "sandstone"],
            state="readonly",
            width=20
        )
        theme_combo.pack(side=LEFT, padx=10)
        
        # Notification Settings
        notif_frame = ttb.Labelframe(settings_frame, text="Notification Settings", padding=15)
        notif_frame.pack(fill=X, padx=20, pady=10)
        
        # Email notifications
        email_var = tk.BooleanVar(value=True)
        ttb.Checkbutton(
            notif_frame,
            text="Enable email notifications",
            variable=email_var,
            bootstyle="primary"
        ).pack(anchor=W, pady=5)
        
        # Desktop notifications
        desktop_var = tk.BooleanVar(value=True)
        ttb.Checkbutton(
            notif_frame,
            text="Enable desktop notifications",
            variable=desktop_var,
            bootstyle="primary"
        ).pack(anchor=W, pady=5)
        
        # Save button
        save_frame = ttb.Frame(settings_frame)
        save_frame.pack(fill=X, padx=20, pady=20)
        
        ttb.Button(
            save_frame,
            text="Save Changes",
            command=lambda: self.save_settings(theme_var.get(), email_var.get(), desktop_var.get()),
            bootstyle="success",
            width=15
        ).pack(side=RIGHT)
        
        # Update sidebar
        self.update_sidebar_content()

    def save_settings(self, theme, email_notif, desktop_notif):
        # Save settings to configuration
        try:
            settings = {
                'theme': theme,
                'email_notifications': email_notif,
                'desktop_notifications': desktop_notif
            }
            
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            
            # Apply theme change
            if theme != self.style.theme.name:
                self.style.theme_use(theme)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

    def create_todays_schedule(self, parent, today_tasks):
        # Create a more visually appealing schedule card
        schedule_frame = ttb.Labelframe(
            parent,
            text="Today's Schedule",
            padding=15,
            bootstyle="info"
        )
        schedule_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        # Add search/filter capabilities
        filter_frame = ttb.Frame(schedule_frame)
        filter_frame.pack(fill=X, pady=(0, 10))
        
        search_var = tk.StringVar()
        search_entry = ttb.Entry(
            filter_frame, 
            textvariable=search_var, 
            bootstyle="info",
            width=30
        )
        search_entry.pack(side=LEFT)
        search_entry.insert(0, "Search tasks...")
        
        # Clear search field on focus
        def on_entry_focus(event):
            if search_entry.get() == "Search tasks...":
                search_entry.delete(0, tk.END)
                
        def on_entry_blur(event):
            if not search_entry.get():
                search_entry.insert(0, "Search tasks...")
        
        search_entry.bind("<FocusIn>", on_entry_focus)
        search_entry.bind("<FocusOut>", on_entry_blur)
        
        # Add filter function
        def filter_tasks():
            search_term = search_var.get().lower()
            if search_term == "search tasks...":
                search_term = ""
                
            # Clear existing task items
            for widget in task_list_frame.winfo_children():
                widget.destroy()
                
            filtered_tasks = [t for t in today_tasks if search_term in t.get('title', '').lower()]
            
            if not filtered_tasks:
                empty_frame = ttb.Frame(task_list_frame, bootstyle="light")
                empty_frame.pack(fill=X, pady=20)
                
                ttb.Label(
                    empty_frame,
                    text="No matching tasks found",
                    font=("Helvetica", 12),
                    bootstyle="secondary"
                ).pack(expand=True)
            else:
                try:
                    sorted_tasks = self.sort_tasks_by_time(filtered_tasks)
                    for task in sorted_tasks:
                        self.create_enhanced_task_item(task_list_frame, task)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to sort tasks: {str(e)}")
                    for task in filtered_tasks:
                        self.create_enhanced_task_item(task_list_frame, task)
        
        # Add search button
        ttb.Button(
            filter_frame,
            text="Search",
            command=filter_tasks,
            bootstyle="info-outline"
        ).pack(side=LEFT, padx=5)
        
        # Add dropdown for sorting options
        sort_var = tk.StringVar(value="Time")
        sort_options = ["Time", "Priority", "Title"]
        sort_menu = ttb.OptionMenu(
            filter_frame,
            sort_var,
            *sort_options
        )
        sort_menu.pack(side=RIGHT)
        
        ttb.Label(
            filter_frame,
            text="Sort by:",
            bootstyle="secondary"
        ).pack(side=RIGHT, padx=5)
        
        # Main task list with regular frame instead of ScrolledFrame
        task_list_frame = ttb.Frame(schedule_frame)
        task_list_frame.pack(fill=BOTH, expand=YES)
        
        if not today_tasks:
            empty_frame = ttb.Frame(task_list_frame, bootstyle="light")
            empty_frame.pack(fill=X, pady=20)
            
            ttb.Label(
                empty_frame,
                text="No tasks scheduled for today",
                font=("Helvetica", 12),
                bootstyle="secondary"
            ).pack(expand=True)
            
            # Add "quick add" button for empty state
            ttb.Button(
                empty_frame,
                text="+ Add Task",
                command=self.add_task_dialog,
                bootstyle="info"
            ).pack(pady=10)
        else:
            try:
                sorted_tasks = self.sort_tasks_by_time(today_tasks)
                for task in sorted_tasks:
                    self.create_enhanced_task_item(task_list_frame, task)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to sort tasks: {str(e)}")
                for task in today_tasks:
                    self.create_enhanced_task_item(task_list_frame, task)

    def create_productivity_chart(self, parent):
        # Create chart frame
        chart_frame = ttb.Labelframe(
            parent,
            text="Productivity Trends",
            padding=15,
            bootstyle="primary"
        )
        chart_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        # Get task completion data for the last 7 days
        today = datetime.now().date()
        days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
        day_names = [day.strftime("%a") for day in days]
        
        # Get completed tasks per day
        completed_counts = []
        for day in days:
            day_str = day.strftime("%Y-%m-%d")
            count = len([t for t in self.tasks if t.get('completed', False) and 
                        t.get('completion_date', '') == day_str])
            completed_counts.append(count)
        
        # Create matplotlib figure for the chart
        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        ax.bar(day_names, completed_counts, color='#1E88E5')
        ax.set_title('Tasks Completed Last 7 Days')
        ax.set_ylabel('Completed Tasks')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Create colorful threshold line for daily goal
        daily_goal = 3  # Example: 3 tasks per day goal
        ax.axhline(y=daily_goal, color='#FF5722', linestyle='--', alpha=0.8)
        ax.text(0, daily_goal + 0.2, 'Daily Goal', color='#FF5722')
        
        # Embed the chart in Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)
        
        # Add chart selector
        chart_selector_frame = ttb.Frame(chart_frame)
        chart_selector_frame.pack(fill=X, pady=(10, 0))
        
        # Different chart options
        chart_options = ["Last 7 Days", "Last 30 Days", "By Category"]
        chart_var = tk.StringVar(value=chart_options[0])
        
        for i, option in enumerate(chart_options):
            ttb.Radiobutton(
                chart_selector_frame,
                text=option,
                variable=chart_var,
                value=option,
                bootstyle="primary-toolbutton"
            ).pack(side=LEFT, padx=5)

    def create_upcoming_deadlines(self, parent):
        # Create upcoming deadlines section
        deadlines_frame = ttb.Labelframe(
            parent,
            text="Upcoming Deadlines",
            padding=15,
            bootstyle="danger"
        )
        deadlines_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        # Get tasks with upcoming deadlines (within next 7 days)
        today = datetime.now().date()
        upcoming_tasks = []
        
        for task in self.tasks:
            if task.get('completed', False):
                continue
                
            try:
                due_date_str = task.get('due_date', '')
                if due_date_str:
                    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                    days_remaining = (due_date - today).days
                    
                    if 0 <= days_remaining <= 7:
                        task['days_remaining'] = days_remaining
                        upcoming_tasks.append(task)
            except ValueError:
                continue
        
        # Sort by days remaining
        upcoming_tasks.sort(key=lambda x: x.get('days_remaining', 0))
        
        # Display upcoming deadlines
        if not upcoming_tasks:
            empty_frame = ttb.Frame(deadlines_frame, bootstyle="light")
            empty_frame.pack(fill=X, pady=20)
            
            ttb.Label(
                empty_frame,
                text="No upcoming deadlines in the next 7 days",
                font=("Helvetica", 12),
                bootstyle="secondary"
            ).pack(expand=True)
        else:
            # Create scrollable frame for deadline items
            deadlines_list = ScrolledFrame(deadlines_frame, bootstyle="rounded")
            deadlines_list.pack(fill=BOTH, expand=YES)
            
            for task in upcoming_tasks:
                days = task.get('days_remaining', 0)
                
                # Create deadline item frame
                deadline_frame = ttb.Frame(deadlines_list, bootstyle="light")
                deadline_frame.pack(fill=X, pady=5, padx=5)
                
                # Left content
                left_content = ttb.Frame(deadline_frame)
                left_content.pack(side=LEFT, fill=X, expand=YES, padx=10, pady=10)
                
                ttb.Label(
                    left_content,
                    text=task.get('title', 'Untitled Task'),
                    font=("Helvetica", 12, "bold"),
                    bootstyle="dark"
                ).pack(anchor="w")
                
                # Right content with days remaining badge
                right_content = ttb.Frame(deadline_frame)
                right_content.pack(side=RIGHT, padx=10, pady=10)
                
                # Change color based on urgency
                badge_color = "danger" if days <= 1 else "warning" if days <= 3 else "info"
                day_text = "Today!" if days == 0 else "Tomorrow!" if days == 1 else f"{days} days"
                
                ttb.Label(
                    right_content,
                    text=day_text,
                    bootstyle=f"{badge_color}-strong",
                    padding=5
                ).pack()

    def create_goal_progress_tracker(self, parent, goals_in_progress, achieved_goals):
        # Create goal progress tracker
        goals_frame = ttb.Labelframe(
            parent,
            text="Goal Progress",
            padding=15,
            bootstyle="success"
        )
        goals_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        if not goals_in_progress and not achieved_goals:
            empty_frame = ttb.Frame(goals_frame, bootstyle="light")
            empty_frame.pack(fill=X, pady=20)
            
            ttb.Label(
                empty_frame,
                text="No goals set yet",
                font=("Helvetica", 12),
                bootstyle="secondary"
            ).pack(expand=True)
            
            # Quick add button
            ttb.Button(
                empty_frame,
                text="+ Set New Goal",
                command=self.add_goal_dialog,
                bootstyle="success"
            ).pack(pady=10)
        else:
            # Create scrollable frame for goals
            goals_list = ScrolledFrame(goals_frame, bootstyle="rounded")
            goals_list.pack(fill=BOTH, expand=YES)
            
            # Process and show in-progress goals first
            for goal in goals_in_progress:
                title = goal.get('title', 'Untitled Goal')
                target_date_str = goal.get('target_date', 'No target date')
                progress = goal.get('progress', 0)
                
                # Create goal progress item
                goal_frame = ttb.Frame(goals_list, bootstyle="light")
                goal_frame.pack(fill=X, pady=5, padx=5)
                
                # Goal title and details
                details_frame = ttb.Frame(goal_frame)
                details_frame.pack(fill=X, padx=10, pady=(10, 5))
                
                ttb.Label(
                    details_frame,
                    text=title,
                    font=("Helvetica", 12, "bold"),
                    bootstyle="dark"
                ).pack(side=LEFT)
                
                ttb.Label(
                    details_frame,
                    text=f"Target: {target_date_str}",
                    font=("Helvetica", 10),
                    bootstyle="secondary"
                ).pack(side=RIGHT)
                
                # Progress bar
                progress_frame = ttb.Frame(goal_frame)
                progress_frame.pack(fill=X, padx=10, pady=(0, 10))
                
                progress_bar = ttb.Progressbar(
                    progress_frame,
                    value=progress,
                    bootstyle="success-striped"
                )
                progress_bar.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))
                
                ttb.Label(
                    progress_frame,
                    text=f"{progress}%",
                    bootstyle="success"
                ).pack(side=LEFT)
                
                # Quick update button
                ttb.Button(
                    progress_frame,
                    text="Update",
                    command=lambda g=goal: self.update_goal_progress(g),
                    bootstyle="success-outline"
                ).pack(side=RIGHT, padx=5)

    def update_goal_progress(self, goal):
        # Create a dialog to update goal progress
        dialog = ttb.Toplevel(title="Update Goal Progress")
        dialog.geometry("400x250")
        
        # Center the dialog
        dialog.place_window_center()
        
        # Create form frame
        form_frame = ttb.Frame(dialog, padding=20)
        form_frame.pack(fill=BOTH, expand=YES)
        
        # Goal title display
        ttb.Label(
            form_frame,
            text=goal.get('title', 'Update Goal Progress'),
            font=("Helvetica", 14, "bold")
        ).pack(fill=X, pady=(0, 20))
        
        # Current progress display
        current_progress = goal.get('progress', 0)
        ttb.Label(
            form_frame,
            text=f"Current Progress: {current_progress}%",
            bootstyle="success"
        ).pack(fill=X)
        
        # Progress slider
        progress_var = tk.IntVar(value=current_progress)
        progress_slider = ttb.Scale(
            form_frame,
            from_=0,
            to=100,
            variable=progress_var,
            bootstyle="success"
        )
        progress_slider.pack(fill=X, pady=10)
        
        # Progress value display
        progress_label = ttb.Label(
            form_frame,
            textvariable=progress_var,
            bootstyle="success"
        )
        progress_label.pack()
        
        # Add % sign to the label
        def update_label(*args):
            progress_label.configure(text=f"{progress_var.get()}%")
        
        progress_var.trace_add("write", update_label)
        update_label()
        
        # Button frame
        button_frame = ttb.Frame(form_frame)
        button_frame.pack(fill=X, pady=(20, 0))
        
        # Cancel button
        ttb.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bootstyle="secondary-outline"
        ).pack(side=LEFT, padx=5)
        
        # Save button
        def save_progress():
            # Update the goal progress
            goal['progress'] = progress_var.get()
            
            # Set completed if 100%
            if progress_var.get() == 100:
                goal['completed'] = True
            else:
                goal['completed'] = False
                
            # Save data and refresh the dashboard
            self.save_data()
            self.show_dashboard()
            dialog.destroy()
        
        ttb.Button(
            button_frame,
            text="Save Progress",
            command=save_progress,
            bootstyle="success"
        ).pack(side=RIGHT, padx=5)

    def sort_tasks_by_time(self, tasks):
        def get_time_value(task):
            try:
                time_str = task.get('time', '00:00')
                if ':' not in time_str:
                    return datetime.strptime('00:00', '%H:%M')
                return datetime.strptime(time_str, '%H:%M')
            except ValueError:
                return datetime.strptime('00:00', '%H:%M')
        
        return sorted(tasks, key=get_time_value)

    def create_enhanced_task_item(self, parent, task):
        # Determine task priority and set appropriate styling
        priority = task.get('priority', 'Medium')
        completed = task.get('completed', False)
        
        # Set color based on priority and completion status
        if completed:
            border_color = "#888888"
            background_color = "#f0f0f0"
        elif priority == "High":
            border_color = "#e74c3c"
            background_color = "#fdedec"
        elif priority == "Medium":
            border_color = "#f39c12"
            background_color = "#fef5e7"
        else:  # Low
            border_color = "#3498db"
            background_color = "#ebf5fb"
        
        # Create task frame with custom styling
        task_frame = ttb.Frame(parent, height=90, relief="solid", borderwidth=1)
        task_frame.pack(fill=X, padx=10, pady=5)
        task_frame.pack_propagate(False)  # Maintain fixed height
        
        # Add a canvas for the left border color indicator
        indicator = tk.Canvas(task_frame, width=4, highlightthickness=0)
        indicator.pack(side=LEFT, fill=Y)
        indicator.create_rectangle(0, 0, 10, 500, fill=border_color, outline="")
        
        # Create content frame
        content = ttb.Frame(task_frame, padding=10)
        content.pack(side=LEFT, fill=BOTH, expand=YES)
        
        # Title with strikethrough if completed
        title_text = task.get('title', 'Untitled Task')
        if completed:
            title_text = "✓ " + title_text
        
        title = ttb.Label(
            content,
            text=title_text,
            font=("Helvetica", 12, "bold"),
            anchor="w",
            bootstyle="secondary" if completed else "default"
        )
        title.pack(anchor=W, pady=(0, 5))
        
        # Description (if available)
        description = task.get('description', '').strip()
        if description:
            desc_label = ttb.Label(
                content,
                text=description[:75] + ('...' if len(description) > 75 else ''),
                bootstyle="secondary",
                anchor="w"
            )
            desc_label.pack(anchor=W, fill=X)
        
        # Time and additional info at bottom
        info_frame = ttb.Frame(content)
        info_frame.pack(fill=X, pady=(5, 0), anchor=W)
        
        # Format time nicely
        time_str = task.get('time', '')
        if time_str:
            try:
                time_obj = datetime.strptime(time_str, '%H:%M')
                time_str = time_obj.strftime('%I:%M %p')
            except ValueError:
                pass
        
        # Add time label
        time_label = ttb.Label(
            info_frame,
            text=time_str,
            bootstyle="secondary",
            font=("Helvetica", 10)
        )
        time_label.pack(side=LEFT)
        
        # Add priority indicator
        if not completed:
            priority_text = f"• {priority} Priority"
            priority_label = ttb.Label(
                info_frame,
                text=priority_text,
                bootstyle="secondary",
                font=("Helvetica", 10)
            )
            priority_label.pack(side=LEFT, padx=(10, 0))
        
        # Button frame on the right
        btn_frame = ttb.Frame(task_frame)
        btn_frame.pack(side=RIGHT, padx=10, fill=Y)
        
        # Add action buttons
        if not completed:
            complete_btn = ttb.Button(
                btn_frame,
                text="Complete",
                bootstyle="success-outline",
                command=lambda: self.complete_task(task),
                width=9
            )
            complete_btn.pack(side=TOP, pady=5)
        
        delete_btn = ttb.Button(
            btn_frame,
            text="Delete",
            bootstyle="danger-outline",
            command=lambda: self.delete_task(task),
            width=9
        )
        delete_btn.pack(side=TOP, pady=5)
        
        # Make entire task clickable for details
        for widget in [task_frame, content, title, info_frame]:
            widget.bind("<Button-1>", lambda e, t=task: self.show_task_details(t))
            widget.bind("<Enter>", lambda e, tf=task_frame: self.on_task_hover(tf, True))
            widget.bind("<Leave>", lambda e, tf=task_frame: self.on_task_hover(tf, False))

    def render_task_list(self, container):
        # Clear previous items
        for widget in container.winfo_children():
            widget.destroy()
        
        if not self.filtered_tasks:
            empty_frame = ttb.Frame(container)
            empty_frame.pack(fill=BOTH, expand=YES, pady=50)
            
            # No tasks message with icon
            no_tasks_label = ttb.Label(
                empty_frame,
                text="No tasks found",
                font=("Helvetica", 14),
                bootstyle="secondary"
            )
            no_tasks_label.pack(pady=20)
            
            # Add suggestion
            suggestion_label = ttb.Label(
                empty_frame,
                text="Click on '+ New Task' to create a task",
                font=("Helvetica", 11),
                bootstyle="secondary"
            )
            suggestion_label.pack()
            return
        
        # Sort tasks by date and time
        def get_datetime_value(task):
            try:
                date_str = task.get('date', datetime.now().strftime('%Y-%m-%d'))
                time_str = task.get('time', '00:00')
                if ':' not in time_str:
                    time_str = '00:00'
                return datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
            except ValueError:
                return datetime.max
        
        try:
            sorted_tasks = sorted(self.filtered_tasks, key=get_datetime_value)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sort tasks: {str(e)}")
            sorted_tasks = self.filtered_tasks
        
        # Group tasks by date
        task_groups = {}
        for task in sorted_tasks:
            date_str = task.get('date')
            if date_str not in task_groups:
                task_groups[date_str] = []
            task_groups[date_str].append(task)
        
        # Create task items grouped by date
        for date_str, tasks in task_groups.items():
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                date_header = date_obj.strftime('%A, %B %d, %Y')
                
                # Check if date is today
                if date_str == datetime.now().strftime('%Y-%m-%d'):
                    date_header += " (Today)"
                # Check if date is tomorrow
                elif date_str == (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'):
                    date_header += " (Tomorrow)"
                
                # Create date header
                date_frame = ttb.Frame(container)
                date_frame.pack(fill=X, pady=(15, 5))
                
                date_label = ttb.Label(
                    date_frame,
                    text=date_header,
                    font=("Helvetica", 12, "bold"),
                    bootstyle="secondary"
                )
                date_label.pack(anchor=W, padx=5)
                
                # Add separator
                separator = ttb.Separator(container)
                separator.pack(fill=X, padx=5, pady=5)
                
                # Add tasks for this date
                for task in tasks:
                    self.create_task_item(container, task)
                    
            except Exception as e:
                # If date parsing fails, just show the tasks
                for task in tasks:
                    self.create_task_item(container, task)

    def on_task_hover(self, task_frame, is_hover):
        if is_hover:
            task_frame.configure(relief="raised", borderwidth=1)
        else:
            task_frame.configure(relief="solid", borderwidth=1)

    def show_task_details(self, task):
        dialog = ttb.Toplevel(self.root)
        dialog.title("Task Details")
        dialog.geometry("500x400")
        
        # Add some styling to the dialog
        main_frame = ttb.Frame(dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # Header with task title
        title_frame = ttb.Frame(main_frame)
        title_frame.pack(fill=X, pady=(0, 15))
        
        title_label = ttb.Label(
            title_frame,
            text=task.get('title', 'Untitled Task'),
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(anchor=W)
        
        # Status indicator
        status_text = "✅ Completed" if task.get('completed', False) else "⏳ In Progress"
        status_label = ttb.Label(
            title_frame,
            text=status_text,
            font=("Helvetica", 12),
            bootstyle="success" if task.get('completed', False) else "warning"
        )
        status_label.pack(anchor=W, pady=(5, 0))
        
        # Content frame
        content_frame = ttb.Frame(main_frame)
        content_frame.pack(fill=BOTH, expand=YES)
        
        # Create two columns
        left_col = ttb.Frame(content_frame)
        left_col.pack(side=LEFT, fill=BOTH, expand=YES)
        
        right_col = ttb.Frame(content_frame)
        right_col.pack(side=LEFT, fill=BOTH, expand=YES, padx=(20, 0))
        
        # Date and time
        date_frame = ttb.Labelframe(left_col, text="Date & Time", padding=10)
        date_frame.pack(fill=X, pady=(0, 10))
        
        date_str = task.get('date', '')
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%A, %B %d, %Y')
        except:
            formatted_date = date_str
        
        date_label = ttb.Label(date_frame, text=formatted_date)
        date_label.pack(anchor=W)
        
        time_str = task.get('time', '')
        if time_str:
            try:
                time_obj = datetime.strptime(time_str, '%H:%M')
                time_str = time_obj.strftime('%I:%M %p')
            except:
                pass
                
        if time_str:
            time_label = ttb.Label(date_frame, text=time_str)
            time_label.pack(anchor=W, pady=(5, 0))
        
        # Priority
        priority_frame = ttb.Labelframe(left_col, text="Priority", padding=10)
        priority_frame.pack(fill=X)
        
        priority = task.get('priority', 'Medium')
        priority_label = ttb.Label(
            priority_frame, 
            text=priority,
            bootstyle="danger" if priority == "High" else 
                     "warning" if priority == "Medium" else "info"
        )
        priority_label.pack(anchor=W)
        
        # Description
        desc_frame = ttb.Labelframe(right_col, text="Description", padding=10)
        desc_frame.pack(fill=BOTH, expand=YES)
        
        description = task.get('description', '').strip()
        if not description:
            description = "No description provided."
            
        desc_text = tk.Text(desc_frame, wrap="word", height=8, width=30)
        desc_text.insert("1.0", description)
        desc_text.config(state="disabled")
        desc_text.pack(fill=BOTH, expand=YES)
        
        # Action buttons at bottom
        btn_frame = ttb.Frame(main_frame)
        btn_frame.pack(fill=X, pady=(20, 0))
        
        if not task.get('completed', False):
            complete_btn = ttb.Button(
                btn_frame,
                text="Mark as Completed",
                command=lambda: [self.complete_task(task), dialog.destroy()],
                bootstyle="success"
            )
            complete_btn.pack(side=LEFT, padx=(0, 10))
        
        edit_btn = ttb.Button(
            btn_frame,
            text="Edit Task",
            command=lambda: [dialog.destroy(), self.edit_task(task)],
            bootstyle="info"
        )
        edit_btn.pack(side=LEFT, padx=(0, 10))
        
        delete_btn = ttb.Button(
            btn_frame,
            text="Delete Task",
            command=lambda: [dialog.destroy(), self.delete_task(task)],
            bootstyle="danger"
        )
        delete_btn.pack(side=LEFT)

if __name__ == "__main__":
    root = ttb.Window(themename="cosmo")
    app = LifeManagerApp(root)
    root.mainloop() 