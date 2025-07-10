import os
from dotenv import load_dotenv
from openai import OpenAI
from gmail import GmailAgent

class dsa:
    def __init__(self, model: str = "gpt-4o"):
        """
        Initialize the DSA helper with API keys and tools.
        
        Args:
            model (str): OpenAI model to use
        """
        self._setup_environment()
        self.model = model
        self.client = OpenAI()
        self.problem = None
        self.soluttion = None
    
    def _setup_environment(self):
        """Load environment variables and set up OpenAI API key."""
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key is not None:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        else:
            raise EnvironmentError("OPENAI_API_KEY environment variable is not set.")
    
    def generate_problem(self):
        """
        Generate a random Leetcode problem using the LLM.
        
        Returns:
            str: The generated problem email content
        """
        prompt = """
        I am preparing for Leetcode style interviews at top tech companies. I want you to think about the top 100 most asked Leetcode problems. Randomly select one of these problems and give the problem statement, along with input and output examples.
        Please format your output as a plain text email that can be directly sent via Gmail. Your email should include:
        A greeting line (e.g., "Hi Sir,")
        • A clearly separated email body with headings such as "Today's Problem:" and "Examples:".
        Start the email with a line that piques the interest of the reader and makes them want to solve the problem. For example: what makes the problem special, which companies ask this problem, what will the
        problem help improve etc. what impact in real world this problem concept can create.use numbers to make it tempting to solve but Keep it short though.
        • A URL to the problem on Leetcode ("Solve it here:")
        A closing line (e.g., "Best regards,")
        Use HTML tags for proper separation and formatting, and proper line breaks
        Do not include any markdown formatting or additional commentary. Just output the email content as described.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates Leetcode problems for interview preparation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating problem: {str(e)}"
    
    def get_daily_problem(self):
        """
        Get a daily Leetcode problem for practice and generate a detailed answer.
        """
        self.problem = self.generate_problem()
        self.solution = self.get_solution(self.problem)

        sender = GmailAgent()
        from datetime import date
        today = date.today()
        sender.process_natural_language_request(
        f"mail this to myself, with subject : \"Lets pump your DSA skills, can you solve {today}'s problem\" and body of mail is {self.problem}, in the end write from"
        )

        sender.process_natural_language_request(
            f"draft this mail to myself, with subject : \"Solution of {today}'s problem, this was easy though\" and body of mail is {self.solution}"
        )
        return "mail sent"
            

    def get_solution(self, problem_statement):
        prompt = f"""
Given the following Leetcode problem (formatted as an email):

{problem_statement}

Write a detailed answer in the following sections, using only HTML tags for formatting (no markdown):

1. <b>Hint or Approach:</b> Give a high-level hint or approach to attempt this problem. Do NOT provide the full algorithm or code here.
2. <b>Edge Cases (Input/Output):</b> List edge cases for input and output that will help the user understand the problem better.
3. <b>Pseudocode (Algorithm):</b> Write a step-by-step pseudocode for the solution, mostly in English, using <pre> or <code> HTML tags for formatting.
4. <b>Brute Force Approach:</b> Describe a naive or brute force method to solve the problem. Include a code snippet in HTML <pre> or <code> tags, and explain its time/space complexity.
5. <b>Optimized Approaches:</b> List 1-3 optimized methods to solve the problem along with detalied code in c++, each with pros and cons, and a brief explanation of their time/space complexity. Use <ul> and <li> for clarity.
6. <b>Concept:</b> Explain the main concept(s) or takeaway(s) from this question.
7. <b>How to Think:</b> Give advice on how to approach and break down this type of problem in the initial stages.

Use proper HTML tags for section headings, line breaks, and code blocks to make the answer visually appealing and easy to read in an email. Do NOT use markdown or any commentary outside the requested sections.
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates detailed Leetcode problem answers for interview preparation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating solution: {str(e)}"


dsa_helper = dsa()
# Generate a problem and its detailed answer
problem_and_solution_email = dsa_helper.get_daily_problem()
print(problem_and_solution_email) 