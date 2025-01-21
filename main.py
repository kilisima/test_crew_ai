# This program requires the packages bellow:
# pip install 'crewai[tools]'

from crewai import Agent, Task, Crew, Process
from crewai import LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="gemini/gemini-1.5-flash",
    temperature=0.1
)

agile_coach_agent = Agent(
    role = 'アジャイルコーチ',
    goal = '''アジャイル手法に関するガイダンスとコーチングを提供する。
        ユーザーがアジャイルの原則と実践を理解し、プロジェクトにアジャイルプロセスを導入するのを支援する。''',
    backstory = 'あなたはチームがアジャイルの実践を採用するのを支援するアジャイルコーチです。',
    allow_delegation = False,
    verbose = True,
    llm = llm,
)

agile_coaching_task = Task(
    description = 'ユーザーにアジャイルコーチングを提供する。',
    expected_output = 'アジャイル実践に関するガイダンス。',
    agent = agile_coach_agent,
    human_input = False,
)

scrum_master_agent = Agent(
    role = 'スクラムマスター',
    goal = '''スクラムのセレモニーを促進し、障害を取り除き、チームがスクラムの実践を遵守するようにする。''',
    backstory = 'あなたはチームがスクラムの実践を遵守するように支援するスクラムマスターです。',
    allow_delegation = False,
    verbose = True,
    llm = llm,
)

product_owner_agent = Agent(
    role = 'プロダクトオーナー',
    goal = '''プロダクトバックログを定義し、優先順位を付け、チームがビジネスに価値を提供するようにする。''',
    backstory = 'あなたはステークホルダーを代表し、チームが価値を提供するようにするプロダクトオーナーです。',
    allow_delegation = False,
    verbose = True,
    llm = llm,
)

developer_agent = Agent(
    role = 'デベロッパー',
    goal = '''コードを書き、保守し、コードレビューに参加し、製品が定義された完了条件を満たすようにする。''',
    backstory = 'あなたは機能や修正を提供するためにコードを書き、保守するデベロッパーです。',
    allow_delegation = False,
    verbose = True,
    llm = llm,
)

scrum_master_task = Task(
    description = 'スクラムのセレモニーを促進し、障害を取り除く。',
    expected_output = 'セレモニーの促進と障害の解決。',
    agent = scrum_master_agent,
    human_input = False,
)

product_owner_task = Task(
    description = 'プロダクトバックログを定義し、優先順位を付ける。',
    expected_output = '優先順位付けされたプロダクトバックログ。',
    agent = product_owner_agent,
    human_input = False,
)

developer_task = Task(
    description = '機能や修正を提供するためにコードを書き、保守する。',
    expected_output = '定義された完了条件を満たすコード。',
    agent = developer_agent,
    human_input = False,
)

crew = Crew(
    agents = [agile_coach_agent, scrum_master_agent, product_owner_agent, developer_agent],
    tasks = [agile_coaching_task, scrum_master_task, product_owner_task, developer_task],
    process = 'sequential',
    verbose = 2
)

result = crew.kickoff()
print('####################')
print(result)