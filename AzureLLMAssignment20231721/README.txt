================================================================================
Azure OpenAI - LLM Project
Nova AI
Student: Gonçalo Faustino 20231721
================================================================================

FILES INCLUDED
--------------
interface.py             - GUI launcher (something extra i had fun doing to run the bots)
part1.py                 - Grumpy Teacher Bot code (can be ran separatly)
part2.py                 - TV Control Bot code (can be ran separatly)
knowledge.txt            - Knowledge base for Teacher Bot
.env.example             - Environment variables template
requirements.txt         - Python dependencies

SETUP INSTRUCTIONS
------------------
1. Install Python dependencies:
   pip install -r requirements.txt

2. Copy sample.env to .env:
   copy sample.env .env

3. Edit .env with your Azure credentials:
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_OPENAI_KEY=your-api-key-here


HOW TO RUN
----------
GUI Version:
   python main_gui.py

Command Line:
   python part1.py  (for Grumpy Teacher)
   python part2.py  (for TV Bot)



SUBMISSION
----------
Submit at: http://aka.ms/madasi-nova-ai-homework
Deadline: December 21, 2025, 23:59

================================================================================