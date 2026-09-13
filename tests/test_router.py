from src.agent.router import route_question

def test_graph_route():
    question='Which supplier has highest overheating rate?'
    assert route_question(question) == 'graph'
def test_rag_route():
    question='What should engineers inspect for battery overheating?'
    assert route_question(question) == 'rag'
def test_hybrid_route():
    question=(
        "Is Supplier_B showing an overheating problem "
        "and what should engineers inspect?"
    )
    assert route_question(question) == 'hybrid'