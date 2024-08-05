import os
import tkinter as tk
from tkinter import scrolledtext, ttk
import ttkbootstrap as tb
import httpx
import threading
import json
import nltk
import asyncio
import sounddevice as sd
from RealtimeTTS import TextToAudioStream, CoquiEngine
from concurrent.futures import ThreadPoolExecutor
import subprocess
import webbrowser
import requests


class OllamaTextGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("INFINITY TALKER v0.1")
        self.master.geometry("1280x1100")  # Adjusted from 1200x800 to 900x800

        self.running = False
        self.next_text = None
        self.current_text = None
        self.is_playing = False
        self.text_queue = asyncio.Queue()

        nltk.download("punkt", quiet=True)

        # Initialize the RealTimeTTS engine with CoquiEngine
        self.tts_engine = CoquiEngine()
        self.language = "en"  # Default language
        self.ollama_model = self.get_ollama_models()[0]  # Default model
        self.audio_stream = TextToAudioStream(
            self.tts_engine,
            on_audio_stream_stop=self.on_playback_finished,
            language=self.language,
        )

        # Extended style options
        self.style_options = {
            "safe for work": tk.BooleanVar(value=True),
            "trivias": tk.BooleanVar(value=True),
            "sarcasm": tk.BooleanVar(value=True),
            "irony": tk.BooleanVar(value=True),
            "humor": tk.BooleanVar(value=True),
            "swearing": tk.BooleanVar(value=False),
            "seriousness": tk.BooleanVar(value=False),
            "poetic": tk.BooleanVar(value=False),
            "scientific": tk.BooleanVar(value=False),
            "philosophical": tk.BooleanVar(value=False),
            "dramatic": tk.BooleanVar(value=False),
            "informative": tk.BooleanVar(value=False),
            "fictional": tk.BooleanVar(value=False),
            "romantic": tk.BooleanVar(value=False),
            "thrilling": tk.BooleanVar(value=False),
            "mysterious": tk.BooleanVar(value=False),
            "adventurous": tk.BooleanVar(value=False),
            "comedic": tk.BooleanVar(value=False),
            "historical": tk.BooleanVar(value=False),
            "fantastical": tk.BooleanVar(value=False),
            "realistic": tk.BooleanVar(value=False),
            "uplifting": tk.BooleanVar(value=False),
            "depressing": tk.BooleanVar(value=False),
            "educational": tk.BooleanVar(value=False),
            "controversial": tk.BooleanVar(value=False),
            "political": tk.BooleanVar(value=False),
            "emotional": tk.BooleanVar(value=False),
            "satirical": tk.BooleanVar(value=False),
            "absurd": tk.BooleanVar(value=False),
            "descriptive": tk.BooleanVar(value=False),
            "minimalistic": tk.BooleanVar(value=False),
            "inspirational": tk.BooleanVar(value=False),
            "dark humor": tk.BooleanVar(value=False),
            "whimsical": tk.BooleanVar(value=False),
            "melancholic": tk.BooleanVar(value=False),
            "optimistic": tk.BooleanVar(value=False),
            "pessimistic": tk.BooleanVar(value=False),
            "technical": tk.BooleanVar(value=False),
            "light-hearted": tk.BooleanVar(value=False),
            "serene": tk.BooleanVar(value=False),
            "frightening": tk.BooleanVar(value=False),
            "heroic": tk.BooleanVar(value=False),
            "villainous": tk.BooleanVar(value=False),
            "fantasy": tk.BooleanVar(value=False),
            "science fiction": tk.BooleanVar(value=False),
            "mystery": tk.BooleanVar(value=False),
            "crime": tk.BooleanVar(value=False),
            "documentary": tk.BooleanVar(value=False),
            "biographical": tk.BooleanVar(value=False),
        }

        # Create main frame
        main_frame = ttk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Add header label
        header_label = ttk.Label(
            main_frame, text="INFINITY TALKER", font=("Helvetica", 24, "bold italic")
        )
        header_label.pack(side=tk.TOP, pady=20)

        # Add "Buy Me a Coffee" button
        coffee_button = ttk.Button(
            main_frame,
            text="Buy Me a Coffee",
            command=lambda: webbrowser.open("https://ko-fi.com/roundy"),
            bootstyle="success",
        )
        coffee_button.place(x=10, y=10)

        # Left frame for text areas
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Input text area at the top with description
        input_frame = ttk.Frame(text_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        input_label = ttk.Label(
            input_frame,
            text="Enter Text here and press Start:",
            font=("Helvetica", 12, "bold"),
        )
        input_label.pack(anchor="w", padx=5, pady=2)

        self.input_text = scrolledtext.ScrolledText(
            input_frame, wrap=tk.WORD, height=8, font=("Helvetica", 12)
        )
        self.input_text.pack(fill=tk.X, padx=5, pady=5)

        # Output text area right below input text with description
        output_frame = ttk.Frame(text_frame)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        output_label = ttk.Label(
            output_frame, text="Generated Text:", font=("Helvetica", 12, "bold")
        )
        output_label.pack(anchor="w", padx=5, pady=2)

        self.output_text = scrolledtext.ScrolledText(
            output_frame, wrap=tk.WORD, height=15, font=("Helvetica", 12)
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Right frame for style options and buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        # Style options frame
        style_frame = ttk.LabelFrame(control_frame, text="Style Options", padding=5)
        style_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        # Create checkboxes for style options
        for i, (option, var) in enumerate(self.style_options.items()):
            ttk.Checkbutton(style_frame, text=option.capitalize(), variable=var).grid(
                row=i // 2, column=i % 2, sticky="w", padx=5, pady=2
            )

        # Language selection frame
        language_frame = ttk.LabelFrame(
            control_frame, text="Language Options (EXPERIMENTAL)", padding=5
        )
        language_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        # Dropdown menu for language selection
        self.language_var = tk.StringVar(value="English (en)")
        language_options = [
            ("English (en)", "en"),
            ("Spanish (es)", "es"),
            ("French (fr)", "fr"),
            ("German (de)", "de"),
            ("Italian (it)", "it"),
            ("Portuguese (pt)", "pt"),
            ("Polish (pl)", "pl"),
            ("Turkish (tr)", "tr"),
            ("Russian (ru)", "ru"),
            ("Dutch (nl)", "nl"),
            ("Czech (cs)", "cs"),
            ("Arabic (ar)", "ar"),
            ("Chinese (zh-cn)", "zh-cn"),
            ("Japanese (ja)", "ja"),
            ("Hungarian (hu)", "hu"),
            ("Korean (ko)", "ko"),
            ("Hindi (hi)", "hi"),
        ]
        language_menu = ttk.OptionMenu(
            language_frame,
            self.language_var,
            self.language_var.get(),
            *[lang[0] for lang in language_options],
        )
        language_menu.pack(fill=tk.X, padx=5, pady=5)

        # Ollama model selection frame
        model_frame = ttk.LabelFrame(
            control_frame, text="Ollama Model Options", padding=5
        )
        model_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        # Dropdown menu for Ollama model selection
        self.model_var = tk.StringVar(value=self.ollama_model)
        model_options = self.get_ollama_models()
        model_menu = ttk.OptionMenu(
            model_frame, self.model_var, self.model_var.get(), *model_options
        )
        model_menu.pack(fill=tk.X, padx=5, pady=5)

        # Button to download more models
        download_button = ttk.Button(
            model_frame,
            text="Download More Models",
            command=self.download_more_models,
            bootstyle="primary",
        )
        download_button.pack(fill=tk.X, padx=5, pady=5)

        # Button to open instructions
        instructions_button = ttk.Button(
            model_frame,
            text="View Instructions",
            command=self.open_instructions_window,
            bootstyle="info",
        )
        instructions_button.pack(fill=tk.X, padx=5, pady=5)

        # Buttons frame at the bottom
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        self.start_button = ttk.Button(
            button_frame,
            text="Start",
            command=self.start_generation,
            bootstyle="primary",
        )
        self.start_button.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)

        self.stop_button = ttk.Button(
            button_frame, text="Stop", command=self.stop_generation, bootstyle="danger"
        )
        self.stop_button.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)

        # Create an event loop for asynchronous operations
        self.loop = asyncio.new_event_loop()
        self.executor = ThreadPoolExecutor(max_workers=2)

        # Handle window close event
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def open_instructions_window(self):
        # Create a new window
        instructions_window = tk.Toplevel(self.master)
        instructions_window.title("Instructions")
        instructions_window.geometry("1200x400")

        # Add a scrolled text widget to display the instructions
        instructions_text = scrolledtext.ScrolledText(
            instructions_window, wrap=tk.WORD, font=("Helvetica", 12)
        )
        instructions_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Read the content of instruction.txt and display it
        try:
            with open("instruction.txt", "r") as file:
                content = file.read()
                instructions_text.insert(tk.END, content)
        except FileNotFoundError:
            instructions_text.insert(tk.END, "instruction.txt file not found.")

    def get_ollama_models(self):
        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]
                return model_names
            else:
                print(
                    f"Failed to fetch Ollama models. Status code: {response.status_code}"
                )
                return []
        except Exception as e:
            print(f"Error fetching Ollama models: {e}")
            return []

    def download_more_models(self):
        webbrowser.open("https://ollama.com/library")

    async def start_generation_async(self):
        if not self.running:
            self.running = True
            initial_text = self.input_text.get("1.0", tk.END).strip()
            await self.process_initial_text(initial_text)

    def start_generation(self):
        self.language = self.language_var.get().split(" ")[-1][
            1:-1
        ]  # Get the selected language code
        self.ollama_model = self.model_var.get()  # Get the selected Ollama model
        self.audio_stream.language = (
            self.language
        )  # Update language for TextToAudioStream
        asyncio.run_coroutine_threadsafe(self.start_generation_async(), self.loop)

    def stop_generation(self):
        self.running = False
        self.audio_stream.stop()

    async def process_initial_text(self, initial_text):
        # Generate first text from Llama
        first_generated_text = await self.call_llama_api(initial_text)

        # Combine initial and first generated text
        combined_text = f"{initial_text}\n\n{first_generated_text}"

        # Update output and start playing
        self.master.after(0, self.update_output_and_play, combined_text)

        # Generate next text while playing
        asyncio.create_task(self.generate_and_cache_text(first_generated_text))

    def generate_audio_and_play(self, text):
        if self.running:
            self.is_playing = True
            self.audio_stream.feed(text)
            self.audio_stream.play_async(
                language=self.language
            )  # Pass language explicitly

    def on_playback_finished(self):
        self.is_playing = False
        if self.running:
            asyncio.run_coroutine_threadsafe(self.play_next(), self.loop)

    async def play_next(self):
        if not self.text_queue.empty():
            next_text = await self.text_queue.get()
            self.master.after(0, self.update_output_and_play, next_text)

    async def generate_and_cache_text(self, text):
        next_text = await self.call_llama_api(text)
        await self.text_queue.put(next_text)

    def update_output_and_play(self, text):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
        self.current_text = text
        self.generate_audio_and_play(text)
        asyncio.run_coroutine_threadsafe(
            self.generate_and_cache_text(text.split("\n\n")[-1]), self.loop
        )

    def get_active_style_options(self):
        return [option for option, var in self.style_options.items() if var.get()]

    async def call_llama_api(self, text):
        active_styles = self.get_active_style_options()
        style_instruction = ", ".join(active_styles)
        prompt = f"Continue the following text logically for 100 words in {self.language} language ({style_instruction}):\n\n{text}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": self.ollama_model,
                        "keep_alive": 0,
                        "prompt": prompt,
                    },
                    timeout=None,
                )
                response.raise_for_status()

                generated_text = ""
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        if "response" in data:
                            generated_text += data["response"]

                return generated_text

            except Exception as e:
                print(f"Error occurred: {e}")
                self.running = False
                return ""

    def on_closing(self):
        # Stop the audio stream
        self.audio_stream.stop()
        # Stop the asyncio loop
        self.loop.stop()
        # Shut down the executor
        self.executor.shutdown(wait=False)
        # Destroy the Tkinter window
        self.master.destroy()

    def run(self):
        def run_loop(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        threading.Thread(target=run_loop, args=(self.loop,), daemon=True).start()


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = OllamaTextGenerator(root)
    app.run()
    root.mainloop()
