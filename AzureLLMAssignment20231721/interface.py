import tkinter as tk
from tkinter import scrolledtext, messagebox
import sys
import os
from part1 import GrumpyTeacherBot

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class GrumpyTeacherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Grumpy AI Teacher Bot")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c2c2c')
        
        # Initialize bot
        self.bot = GrumpyTeacherBot()
        self.setup_ui()
        
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
        input_frame.pack(padx=20, pady=(0, 20), fill=tk.X)
        
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
        self.user_input.bind('<Control-Return>', lambda e: self.send_message())
        
        # Send button
        send_btn = tk.Button(
            input_frame,
            text="Send →",
            command=self.send_message,
            bg='#ff4444',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            padx=20
        )
        send_btn.pack(side=tk.RIGHT)
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Ctrl+Enter or click Send | Type 'quit' to exit | AI topics only!",
            font=('Arial', 9),
            fg='#888888',
            bg='#2c2c2c'
        )
        instructions.pack()
        
        # Welcome message
        self.add_to_chat("🤖 Teacher Bot", "AI Grumpy Teacher Bot ready. Ask about AI or get lost!")
        self.add_to_chat("💭 You", "Type your AI question below...")
        
        # Focus input
        self.user_input.focus_set()
    
    def add_to_chat(self, sender, message):
        """Add message to chat display with sender prefix"""
        timestamp = self.get_timestamp()
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: {message}\n\n")
        self.chat_display.see(tk.END)
    
    def get_timestamp(self):
        """Get current time for chat"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def send_message(self, event=None):
        """Send user message to bot"""
        user_msg = self.user_input.get("1.0", tk.END).strip()
        if not user_msg:
            return
        
        self.add_to_chat("💭 You", user_msg)
        self.user_input.delete("1.0", tk.END)
    
        
        if user_msg.lower() in ['quit', 'exit', 'bye']:
            self.add_to_chat("🤖 Teacher Bot", "Finally! Goodbye!")
            self.root.quit()
            return
        
        try:
            reply = self.bot.get_reply(user_msg)
            self.add_to_chat("🤖 Teacher Bot", reply)
        except Exception as e:
            self.add_to_chat("🤖 Teacher Bot", f"Ugh, something broke: {str(e)}")
    

def main():
    root = tk.Tk()
    app = GrumpyTeacherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
