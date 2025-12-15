import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime

# =======================
# MAIN MENU LAUNCHER
# =======================

class MainMenuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Bot Launcher")
        self.root.geometry("500x400")
        self.root.configure(bg='#1e1e1e')
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="🤖 AI Bot Launcher 🤖", 
            font=('Arial', 20, 'bold'),
            fg='#ffffff',
            bg='#1e1e1e'
        )
        title_label.pack(pady=40)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.root, 
            text="Choose which bot to run:", 
            font=('Arial', 12),
            fg='#aaaaaa',
            bg='#1e1e1e'
        )
        subtitle_label.pack(pady=10)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg='#1e1e1e')
        button_frame.pack(pady=30)
        
        # Grumpy Teacher Button
        grumpy_btn = tk.Button(
            button_frame,
            text="🤬 Grumpy AI Teacher Bot\n(AI Questions Only)",
            command=self.launch_grumpy_teacher,
            bg='#ff4444',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief=tk.FLAT,
            padx=30,
            pady=20,
            width=25,
            cursor='hand2'
        )
        grumpy_btn.pack(pady=10)
        
        # TV Control Button
        tv_btn = tk.Button(
            button_frame,
            text="📺 TV Control Bot\n(Control Your Television)",
            command=self.launch_tv_bot,
            bg='#4444ff',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief=tk.FLAT,
            padx=30,
            pady=20,
            width=25,
            cursor='hand2'
        )
        tv_btn.pack(pady=10)
        
        # Exit Button
        exit_btn = tk.Button(
            button_frame,
            text="❌ Exit",
            command=self.root.quit,
            bg='#666666',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            width=25,
            cursor='hand2'
        )
        exit_btn.pack(pady=20)
    
    def launch_grumpy_teacher(self):
        """Launch Grumpy Teacher Bot"""
        try:
            from part1 import GrumpyTeacherBot
            self.root.withdraw()  # Hide menu
            new_window = tk.Toplevel(self.root)
            GrumpyTeacherGUI(new_window, self.root)
        except ImportError as e:
            messagebox.showerror("Error", f"Could not import GrumpyTeacherBot from part1.py\n\nError: {str(e)}\n\nMake sure part1.py exists in the same folder!")
    
    def launch_tv_bot(self):
        """Launch TV Bot"""
        try:
            from part2 import Television, TVAIBOT, client
            self.root.withdraw()  # Hide menu
            new_window = tk.Toplevel(self.root)
            TVBotGUI(new_window, self.root)
        except ImportError as e:
            messagebox.showerror("Error", f"Could not import TV bot from part2.py\n\nError: {str(e)}\n\nMake sure part2.py exists with Television, TVAIBOT, and client!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch TV bot: {str(e)}")


# =======================
# GRUMPY TEACHER GUI
# =======================

class GrumpyTeacherGUI:
    def __init__(self, root, parent_menu):
        self.root = root
        self.parent_menu = parent_menu
        self.root.title("Grumpy AI Teacher Bot")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c2c2c')
        
        # Initialize bot
        from part1 import GrumpyTeacherBot
        self.bot = GrumpyTeacherBot()
        self.setup_ui()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.back_to_menu)
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="🤬 Grumpy AI Teacher Bot 🤬\n(Ask about AI only!)", 
            font=('Arial', 14, 'bold'),
            fg='#ff4444',
            bg='#2c2c2c'
        )
        title_label.pack(pady=10)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            self.root,
            height=20,
            width=80,
            font=('Consolas', 11),
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='white',
            wrap=tk.WORD
        )
        self.chat_display.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#2c2c2c')
        input_frame.pack(padx=20, pady=(0, 10), fill=tk.X)
        
        # User input
        self.user_input = tk.Text(
            input_frame,
            height=3,
            font=('Consolas', 11),
            bg='#3c3c3c',
            fg='#ffffff',
            insertbackground='white'
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.user_input.bind('<Return>', self.send_message)
        self.user_input.bind('<Shift-Return>', lambda e: None)  # Allow Shift+Enter for new line
        
        # Send button
        send_btn = tk.Button(
            input_frame,
            text="Send →",
            command=self.send_message,
            bg='#ff4444',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            padx=20,
            cursor='hand2'
        )
        send_btn.pack(side=tk.RIGHT)
        
        # Bottom frame
        bottom_frame = tk.Frame(self.root, bg='#2c2c2c')
        bottom_frame.pack(pady=5)
        
        # Back button
        back_btn = tk.Button(
            bottom_frame,
            text="← Back to Menu",
            command=self.back_to_menu,
            bg='#666666',
            fg='white',
            font=('Arial', 9),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        back_btn.pack()
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Press Enter to send | Shift+Enter for new line | Type 'quit' to exit",
            font=('Arial', 9),
            fg='#888888',
            bg='#2c2c2c'
        )
        instructions.pack(pady=5)
        
        # Welcome message
        self.add_to_chat("🤖 Teacher Bot", "AI Grumpy Teacher Bot ready. Ask about AI or get lost!")
        
        # Focus input
        self.user_input.focus_set()
    
    def add_to_chat(self, sender, message):
        """Add message to chat display with sender prefix"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: {message}\n\n")
        self.chat_display.see(tk.END)
    
    def send_message(self, event=None):
        """Send user message to bot"""
        user_msg = self.user_input.get("1.0", tk.END).strip()
        if not user_msg:
            return "break"
        
        self.add_to_chat("💭 You", user_msg)
        self.user_input.delete("1.0", tk.END)
        
        if user_msg.lower() in ['quit', 'exit', 'bye']:
            self.add_to_chat("🤖 Teacher Bot", "Finally! Goodbye!")
            self.root.after(1000, self.back_to_menu)
            return "break"
        
        try:
            reply = self.bot.get_reply(user_msg)
            self.add_to_chat("🤖 Teacher Bot", reply)
        except Exception as e:
            self.add_to_chat("🤖 Teacher Bot", f"Ugh, something broke: {str(e)}")
        
        return "break"
    
    def back_to_menu(self):
        """Return to main menu"""
        self.root.destroy()
        self.parent_menu.deiconify()


# =======================
# TV BOT GUI
# =======================

class TVBotGUI:
    def __init__(self, root, parent_menu):
        self.root = root
        self.parent_menu = parent_menu
        self.root.title("TV Control Bot")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a2e')
        
        # Initialize TV and bot
        from part2 import Television, TVAIBOT, client
        self.tv = Television()
        self.bot = TVAIBOT(client)
        
        self.setup_ui()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.back_to_menu)
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="📺 TV Control Bot 📺", 
            font=('Arial', 16, 'bold'),
            fg='#4444ff',
            bg='#1a1a2e'
        )
        title_label.pack(pady=10)
        
        # TV Status Panel
        status_frame = tk.Frame(self.root, bg='#0f3460', relief=tk.RAISED, bd=3)
        status_frame.pack(padx=20, pady=10, fill=tk.X)
        
        status_title = tk.Label(
            status_frame,
            text="📊 TV Status",
            font=('Arial', 12, 'bold'),
            fg='#ffffff',
            bg='#0f3460'
        )
        status_title.pack(pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text=self.tv.get_status(),
            font=('Consolas', 11),
            fg='#00ff00',
            bg='#0f3460',
            justify=tk.LEFT
        )
        self.status_label.pack(pady=10, padx=20)
        
        # Chat display
        chat_label = tk.Label(
            self.root,
            text="💬 Conversation",
            font=('Arial', 12, 'bold'),
            fg='#ffffff',
            bg='#1a1a2e'
        )
        chat_label.pack(pady=(10, 5))
        
        self.chat_display = scrolledtext.ScrolledText(
            self.root,
            height=15,
            width=90,
            font=('Consolas', 10),
            bg='#16213e',
            fg='#ffffff',
            insertbackground='white',
            wrap=tk.WORD
        )
        self.chat_display.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#1a1a2e')
        input_frame.pack(padx=20, pady=(10, 5), fill=tk.X)
        
        # User input
        self.user_input = tk.Text(
            input_frame,
            height=3,
            font=('Consolas', 11),
            bg='#0f3460',
            fg='#ffffff',
            insertbackground='white'
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.user_input.bind('<Return>', self.send_message)
        self.user_input.bind('<Shift-Return>', lambda e: None)
        
        # Button container
        button_container = tk.Frame(input_frame, bg='#1a1a2e')
        button_container.pack(side=tk.RIGHT)
        
        # Send button
        send_btn = tk.Button(
            button_container,
            text="Send →",
            command=self.send_message,
            bg='#4444ff',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        send_btn.pack()
        
        # Quick Actions Frame
        quick_frame = tk.Frame(self.root, bg='#1a1a2e')
        quick_frame.pack(padx=20, pady=5)
        
        quick_label = tk.Label(
            quick_frame,
            text="⚡ Quick Actions:",
            font=('Arial', 9, 'bold'),
            fg='#aaaaaa',
            bg='#1a1a2e'
        )
        quick_label.pack(side=tk.LEFT, padx=(0, 10))
        
        quick_commands = [
            ("Power ON", "turn on"),
            ("Power OFF", "turn off"),
            ("Show Channels", "show channels"),
            ("Status", "status")
        ]
        
        for label, cmd in quick_commands:
            btn = tk.Button(
                quick_frame,
                text=label,
                command=lambda c=cmd: self.quick_command(c),
                bg='#533483',
                fg='white',
                font=('Arial', 8),
                relief=tk.FLAT,
                padx=10,
                pady=3,
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT, padx=3)
        
        # Bottom frame
        bottom_frame = tk.Frame(self.root, bg='#1a1a2e')
        bottom_frame.pack(pady=5)
        
        # Back button
        back_btn = tk.Button(
            bottom_frame,
            text="← Back to Menu",
            command=self.back_to_menu,
            bg='#666666',
            fg='white',
            font=('Arial', 9),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        back_btn.pack()
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Press Enter to send | Try: 'turn on', 'set volume to 50', 'change to CNN'",
            font=('Arial', 9),
            fg='#888888',
            bg='#1a1a2e'
        )
        instructions.pack(pady=5)
        
        # Welcome message
        self.add_to_chat("🤖 TV Bot", "TV Control Bot ready! Tell me what you want to do with your TV.")
        
        # Focus input
        self.user_input.focus_set()
    
    def add_to_chat(self, sender, message):
        """Add message to chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: {message}\n\n")
        self.chat_display.see(tk.END)
    
    def update_status(self):
        """Update TV status display"""
        self.status_label.config(text=self.tv.get_status())
    
    def quick_command(self, command):
        """Execute quick command"""
        self.user_input.delete("1.0", tk.END)
        self.user_input.insert("1.0", command)
        self.send_message()
    
    def send_message(self, event=None):
        """Send user message to bot"""
        user_msg = self.user_input.get("1.0", tk.END).strip()
        if not user_msg:
            return "break"
        
        self.add_to_chat("💭 You", user_msg)
        self.user_input.delete("1.0", tk.END)
        
        if user_msg.lower() in ['quit', 'exit', 'bye']:
            self.add_to_chat("🤖 TV Bot", "Powering down. Bye! 👋")
            self.root.after(1000, self.back_to_menu)
            return "break"
        
        try:
            # Get AI response
            ai_result = self.bot.process(user_msg)
            response, is_question = self.execute_action(ai_result)
            
            self.add_to_chat("🤖 TV Bot", response)
            
            # Update status if action was performed
            if not is_question:
                self.update_status()
                
        except Exception as e:
            self.add_to_chat("🤖 TV Bot", f"Error: {str(e)}")
        
        return "break"
    
    def execute_action(self, result):
        """Execute TV action from AI result"""
        if "ask" in result:
            return result["ask"], True

        if "error" in result:
            return result["error"], False

        action = result.get("action")

        if action == "turn_on":
            return self.tv.turn_on(), False
        if action == "turn_off":
            return self.tv.turn_off(), False
        if action == "set_volume":
            return self.tv.set_volume(result["value"]), False
        if action == "set_brightness":
            return self.tv.set_brightness(result["value"]), False
        if action == "change_channel":
            return self.tv.change_channel(result["value"]), False
        if action == "show_channels":
            return self.tv.show_channels(), False
        if action == "get_status":
            return self.tv.get_status(), False

        return "Unknown action.", False
    
    def back_to_menu(self):
        """Return to main menu"""
        self.root.destroy()
        self.parent_menu.deiconify()


# =======================
# MAIN ENTRY POINT
# =======================

def main():
    root = tk.Tk()
    MainMenuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()