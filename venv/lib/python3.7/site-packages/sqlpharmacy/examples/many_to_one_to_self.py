from sqlpharmacy.core import Database
from sqlalchemy import Column, String

__metaclass__ = Database.DefaultMeta

@Database.many_to_one('Node', ref_name = 'parent_node', backref_name = 'children_nodes')
class Node:
    name = Column(String(70))

Database.register()

if __name__ == '__main__':
    db = Database('sqlite://')
    db.create_tables()

    root_node = Node(name = 'root')
    node1 = Node(name = 'node1', parent_node = root_node)
    node2 = Node(name = 'node2', parent_node = root_node)
    db.session.add_then_commit(root_node)

    root_node = db.session.query(Node).filter_by(name = 'root').one()
    print('Root node has {0} children nodes, they are {1}'\
        .format(root_node.children_nodes.count(), ', '.join(node.name for node in root_node.children_nodes)))