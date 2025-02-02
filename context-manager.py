class ContextNode:
    def __init__(self, content, metadata=None):
        self.content = content
        self.metadata = metadata or {}
        self.relationships = {}  # Maps relationship types to other nodes
        self.temporal_position = None  # For tracking time-based relationships
        self.confidence_score = 1.0  # Default full confidence
        self.references = []  # Source references if any
        
class ContextGraph:
    def __init__(self):
        self.nodes = {}
        self.current_context = []
        self.context_history = []
        self.relationship_types = set()
        
    def add_node(self, identifier, content, metadata=None):
        """Add a new context node to the graph."""
        node = ContextNode(content, metadata)
        self.nodes[identifier] = node
        return node
        
    def link_nodes(self, source_id, target_id, relationship_type):
        """Create a relationship between two context nodes."""
        if source_id in self.nodes and target_id in self.nodes:
            self.nodes[source_id].relationships[relationship_type] = self.nodes[target_id]
            self.relationship_types.add(relationship_type)
            
    def push_context(self, node_id):
        """Add a context node to the current active context stack."""
        if node_id in self.nodes:
            self.current_context.append(node_id)
            self.context_history.append(('push', node_id))
            
    def pop_context(self):
        """Remove the most recent context from the stack."""
        if self.current_context:
            removed = self.current_context.pop()
            self.context_history.append(('pop', removed))
            return removed
            
    def get_relevant_context(self, query, threshold=0.5):
        """
        Retrieve context nodes relevant to a given query.
        Uses simple similarity scoring for demonstration.
        """
        relevant_nodes = []
        for node_id, node in self.nodes.items():
            # This would be replaced with proper similarity scoring
            similarity = self._calculate_similarity(query, node.content)
            if similarity > threshold:
                relevant_nodes.append((node_id, similarity))
        return sorted(relevant_nodes, key=lambda x: x[1], reverse=True)
    
    def _calculate_similarity(self, text1, text2):
        """
        Placeholder for similarity calculation.
        Would be replaced with proper NLP similarity metrics.
        """
        # Simple word overlap for demonstration
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        overlap = len(words1.intersection(words2))
        total = len(words1.union(words2))
        return overlap / total if total > 0 else 0
        
    def summarize_current_context(self):
        """Generate a summary of the current context stack."""
        summary = []
        for node_id in self.current_context:
            node = self.nodes[node_id]
            summary.append({
                'id': node_id,
                'content': node.content,
                'metadata': node.metadata,
                'confidence': node.confidence_score
            })
        return summary

def example_usage():
    # Create a new context graph
    graph = ContextGraph()
    
    # Add some context nodes
    graph.add_node('user_preference', 'User prefers technical explanations')
    graph.add_node('conversation_topic', 'Discussing machine learning models')
    graph.add_node('prior_knowledge', 'User has programming background')
    
    # Link nodes with relationships
    graph.link_nodes('conversation_topic', 'user_preference', 'influences')
    graph.link_nodes('prior_knowledge', 'conversation_topic', 'informs')
    
    # Push contexts onto the stack
    graph.push_context('user_preference')
    graph.push_context('conversation_topic')
    
    # Get relevant context for a query
    query = "Can you explain neural networks?"
    relevant = graph.get_relevant_context(query)
    
    # Get current context summary
    context_summary = graph.summarize_current_context()
    
    return relevant, context_summary
