import tkinter as tk
from logic import MBTIScorer
from questions import questions

# برای نمایش درست فارسی
import arabic_reshaper
from bidi.algorithm import get_display


def fix_farsi(text):
    """درست کردن جهت و اتصال حروف فارسی"""
    return get_display(arabic_reshaper.reshape(text))


class MBTIGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("💡 تست شخصیت MBTI")
        self.root.geometry("800x500")
        self.root.configure(bg="#f6f6f6")

        self.questions = questions
        self.current_index = 0
        self.answers = []
        self.scorer = MBTIScorer()

        # ---- عنوان ----
        title = tk.Label(
            root,
            text=fix_farsi("💡 تست شخصیت MBTI"),
            font=("Vazir", 22, "bold"),
            bg="#f6f6f6",
            fg="#222"
        )
        title.pack(pady=(20, 10))

        subtitle = tk.Label(
            root,
            text=fix_farsi("برای شروع تست روی دکمه زیر کلیک کنید."),
            font=("Vazir", 14),
            bg="#f6f6f6",
            fg="#444"
        )
        subtitle.pack(pady=(0, 20))

        # ---- کارت اصلی ----
        self.card = tk.Frame(root, bg="white", padx=25, pady=25)
        self.card.pack(fill="both", expand=True, padx=40, pady=20)

        self.question_label = tk.Label(
            self.card,
            text=fix_farsi("برای شروع تست روی دکمه کلیک کنید."),
            font=("Vazir", 16),
            bg="white",
            fg="#111",
            justify="right",
            anchor="e",
            wraplength=700
        )
        self.question_label.pack(pady=(10, 20), anchor="e")

        # ---- فریم دکمه‌ها ----
        self.button_frame = tk.Frame(self.card, bg="white")
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(
            self.card,
            text=fix_farsi("شروع تست"),
            command=self.start_test,
            font=("Vazir", 14),
            bg="#0078d7",
            fg="white",
            activebackground="#005fa3",
            relief="flat",
            width=15,
            height=2,
            cursor="hand2"
        )
        self.start_button.pack(pady=10)

    def start_test(self):
        self.start_button.pack_forget()
        self.show_question()

    def show_question(self):
        if self.current_index < len(self.questions):
            q = self.questions[self.current_index]
            q_text = f"{self.current_index + 1}. {q['question']}"
            self.question_label.config(text=fix_farsi(q_text))
            self.create_option_buttons()
        else:
            self.show_result()

    def create_option_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        options = [("موافقم", 1, "#2e7d32"), ("تاحدی", 2, "#f57f17"), ("مخالفم", 3, "#c62828")]

        for text, val, color in reversed(options):
            btn = tk.Button(
                self.button_frame,
                text=fix_farsi(text),
                command=lambda v=val: self.select_answer(v),
                font=("Vazir", 13),
                bg=color,
                fg="white",
                relief="flat",
                width=12,
                height=2,
                cursor="hand2",
                activebackground=color
            )
            btn.pack(side="right", padx=10)

    def select_answer(self, answer):
        q = self.questions[self.current_index]
        self.scorer.update_score(answer, q["dimension"])
        self.answers.append(answer)
        self.current_index += 1
        self.show_question()

    def show_result(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        personality = self.scorer.determine_personality()

        title = tk.Label(
            self.root,
            text=fix_farsi("🎉 نتیجه تست شما"),
            font=("Vazir", 22, "bold"),
            bg="#f6f6f6",
            fg="#0078d7"
        )
        title.pack(pady=(40, 10))

        result = tk.Label(
            self.root,
            text=fix_farsi(f"تیپ شخصیتی شما: {personality}"),
            font=("Vazir", 18),
            bg="#f6f6f6",
            fg="#333"
        )
        result.pack(pady=10)

        thanks = tk.Label(
            self.root,
            text=fix_farsi("ممنون که در تست MBTI شرکت کردید ❤️"),
            font=("Vazir", 14),
            bg="#f6f6f6",
            fg="#444"
        )
        thanks.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg="#f6f6f6")
        btn_frame.pack(pady=30)

        retry_btn = tk.Button(
            btn_frame,
            text=fix_farsi("تکرار تست"),
            command=self.retry,
            font=("Vazir", 13),
            bg="#0078d7",
            fg="white",
            relief="flat",
            width=12,
            cursor="hand2"
        )
        retry_btn.pack(side="right", padx=10)

        exit_btn = tk.Button(
            btn_frame,
            text=fix_farsi("خروج"),
            command=self.root.destroy,
            font=("Vazir", 13),
            bg="#c62828",
            fg="white",
            relief="flat",
            width=12,
            cursor="hand2"
        )
        exit_btn.pack(side="right", padx=10)

    def retry(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        MBTIGUI(self.root)


def run_gui():
    root = tk.Tk()
    MBTIGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
