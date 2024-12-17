from graphviz import Digraph

class Node:
    def __init__(self, value, parent=None):
        self.parent = parent
        self.value = value
        self.children = []

    def add_child(self, child_node):
        """Ajoute un enfant à ce nœud."""
        self.children.append(child_node)
    
    def remove_child(self, child_node):
        """Supprime un enfant de ce nœud."""
        self.children.remove(child_node)

    def __repr__(self):
        return f"Node({self.value})"

def visualize_tree(root):
    """
    Convertit un arbre basé sur la classe Node en un graphe Graphviz.
    """
    dot = Digraph(format="png")  # Crée un graphe orienté
    dot.attr(rankdir="LR") 

    def add_edges(node):
        # Ajoute le nœud courant
        dot.node(str(id(node)), label=str(node.value[1]["numbers"]))
        for child in node.children:
            # Ajoute un lien entre le parent et l'enfant
            dot.edge(str(id(node)), str(id(child)))
            add_edges(child)  # Appelle récursivement pour les enfants

    add_edges(root)  # Commence à partir de la racine
    return dot
    
def print_tree(node, level=0):
    """Affiche l'arbre avec une indentation pour représenter la hiérarchie."""
    print(" " * (level * 4) + str(node.value[1]["numbers"]))
    for child in node.children:
        print_tree(child, level + 1)

# # Exemple
# root = Node("root")
# child1 = Node("child1")
# child2 = Node("child2")
# root.add_child(child1)
# root.add_child(child2)

# child1.add_child(Node("child1.1"))
# child1.add_child(Node("child1.2"))

# print_tree(root)
