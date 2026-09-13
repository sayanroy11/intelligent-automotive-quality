def route_question(question):
    question=question.lower()
    graph_keywords=[
        'supplier',
        'rate',
        'cases',
        'inspections',
        'highest',
        'lowest',
        'data',
        'pattern'
    ]

    rag_keywords=[
        'inspect',
        'check',
        'cause',
        'causes',
        'recommend',
        'action',
        'troubleshoot',
        'procedure'
    ]

    use_graph=any(
        keyword in question
        for keyword in graph_keywords 
    )
    use_rag=any(
        keyword in question
        for keyword in rag_keywords
    )

    if use_graph and use_rag:
        return 'hybrid'
    if use_graph:
        return 'graph'
    if use_rag:
        return 'rag'

    return 'rag'
if __name__=='__main__':
    questions=[
        'Which supplier has the highest overheating rate?',
        'What should engineers inspect for battery overheating?',
        'Is Supplier_B showing an overheating problem and what should we inspect?'
    ]
    for question in questions:
        print(question)
        print('Route:',route_question(question))
        print()