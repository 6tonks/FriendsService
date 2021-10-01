from py2neo import data, Graph, NodeMatcher, Node, Relationship, RelationshipMatcher
"""
See https://py2neo.org/v4/
"""
import logging

class Neo4JDataResource:
    """
    This object provides a set of helper methods for creating and retrieving nodes and relationships from
    a Neo4j database holding information about players, teams, fans, comments and their relationships.
    """

    # Note:
    # I tend to avoid object mapping frameworks. Object mapping frameworks are fun in the beginning
    # but tend to be annoying after a while. So, I did not create types Player, Team, etc.
    #


    # Connects to the DB and sets a Graph instance variable.
    # Also creates a NodeMatcher and RelationshipMatcher, which are a py2neo framework classes.
    def __init__(self, auth=('neo4j', 'password'), host='localhost', port=7687, debug=False, secure=False):
        self.debug = debug
        self._graph = Graph(secure=secure,
                            auth=auth,
                            host=host,
                            port=port)
        self._node_matcher = NodeMatcher(self._graph)
        self._relationship_matcher = RelationshipMatcher(self._graph)

    def run_q(self, qs, args):
        """

        :param qs: Query string that may have {} slots for parameters.
        :param args: Dictionary of parameters to insert into query string.
        :return:  Result of the query, which executes as a single, standalone transaction.
        """
        try:
            tx = self._graph.begin(readonly=True)
            result = self._graph.run(qs, args)
            return result
        except Exception as e:
            logging.error("Run exception = {}".format(e))

    def run_match(self, labels=None, properties=None):
        """
        Uses a NodeMatcher to find a node matching a "template."
        :param labels: A list of labels that the node must have.
        :param properties: A dictionary of {property_name: property_value} defining the template that the
            node must match.
        :return: An array of Node objects matching the pattern.
        """
        #ut.debug_message("Labels = ", labels)
        #ut.debug_message("Properties = ", json.dumps(properties))

        if labels is not None and properties is not None:
            result = self._node_matcher.match(labels, **properties)
        elif labels is not None and properties is None:
            result = self._node_matcher.match(labels)
        elif labels is None and properties is not None:
            result = self._node_matcher.match(**properties)
        else:
            raise ValueError("Invalid request. Labels and properties cannot both be None.")

        # Convert NodeMatch data into a simple list of Nodes.
        full_result = []
        for r in result:
            full_result.append(r)

        return full_result

    def find_nodes_by_template(self, tmp):
        """

        :param tmp: A template defining the label and properties for Nodes to return. An
         example is { "label": "Fan", "template" { "last_name": "Ferguson", "first_name": "Donald" }}
        :return: A list of Nodes matching the template.
        """
        labels = tmp.get('label', None)
        props = tmp.get("template", None)
        result = self.run_match(labels=labels, properties=props)
        return result

    def create_node(self, label, **kwargs):
        n = Node(label, **kwargs)
        tx = self._graph.begin(readonly=False)
        tx.create(n)
        tx.commit()
        return n

    def create_relationship(self, template_a, template_b, relationship):
        try:
            node_a = self.find_nodes_by_template(template_a)[0]
            node_b = self.find_nodes_by_template(template_b)[0]
            relationship_obj = Relationship(node_a, relationship, node_b)

            tx = self._graph.begin(readonly=False)
            tx.create(relationship_obj)
            tx.commit()

        except Exception as e:
            logging.error("Error NEO4J Create relationship: " + str(e))
            tx.rollback()
            # To distinguish whether it is not found or error
            raise Exception(e)

        return relationship_obj

    def delete_relationship(self, template_a, template_b, relationship):
        try:
            node_a = self.find_nodes_by_template(template_a)[0]
            node_b = self.find_nodes_by_template(template_b)[0]
            relationship_obj = self._relationship_matcher.match(nodes=[node_a, node_b], r_type=relationship).first()

            tx = self._graph.begin(readonly=False)
            tx.separate(relationship_obj)
            tx.commit()

        except Exception as e:
            logging.error("Error NEO4J Delete relationship: " + str(e))
            tx.rollback()
            # To distinguish whether it is not found or error
            raise Exception(e)

        return None

    def find_by_node_relationship_outward(self, template, relationship):
        label = template.get("label", None)
        props = template.get("template", None)
        props_str = ''
        for key, value in props.items():
            props_str += "{}: {},".format(key, value)
        props_str = '{' + props_str[:-1] + '}'

        q = "MATCH (n:{} {})-[:{}]->(m) RETURN m".format(label, props_str, relationship)
        res = self.run_q(q, args=None).data()

        result = []
        for x in res:
            result.append(str(x))
        return result

    def find_by_node_relationship_inward(self, template, relationship):
        label = template.get("label", None)
        props = template.get("template", None)
        props_str = ''
        for key, value in props.items():
            props_str += "{}: {},".format(key, value)
        props_str = '{' + props_str[:-1] + '}'

        q = "MATCH (n:{} {})<-[:{}]-(m) RETURN m".format(label, props_str, relationship)
        res = self.run_q(q, args=None).data()

        result = []
        for x in res:
            result.append(str(x))
        return result

    def update_node(self, label, keys, data):
        props_str = ''
        for key, value in keys.items():
            props_str += "{}: '{}', ".format(key, value)
        props_str = '{' + props_str[:-2] + '}'

        data_str = ''
        for key, value in data.items():
            data_str += "n.{} = '{}', ".format(key, value)
        data_str = data_str[:-2]

        q = "MATCH (n:{} {}) SET {} RETURN n".format(label, props_str, data_str)
        res = self.run_q(q, args=None).data()

        result = []
        for x in res:
            result.append(str(x))

        return result

    def delete_node(self, template):
        nodes = None
        try:
            tx = self._graph.begin(readonly=False)
            nodes = self.find_nodes_by_template(template)
            for node in nodes:
                tx.delete(node)
            tx.commit()
        except Exception as e:
            logging.error("Error NEO4J Delete: " + str(e))
            tx.rollback()
            # To distinguish whether it is not found or error
            raise Exception(e)

        if nodes:
            return len(nodes)
        else:
            return None