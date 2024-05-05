
class Pattern:
    def __init__(self, data, id):
        self.id = id
        self.pattern = data.get('pattern', '')
        self.filters = data.get('filters', [])

    def __str__(self):
        return f"Pattern: {self.id}, {self.pattern}"

# TODO: Create a class for filters
    
class HelperPattern:
    def __init__(self, data):
        self.id = data.get('id', '')
        self.patterns = [Pattern(pattern, self.id + index) for index, pattern in enumerate(data.get('patterns', []))]

    def __str__(self):
        return f"Helper Pattern: {self.id}"

class Rule:
    def __init__(self, data):
        self.metadata = data.get('metadata', {})
        self.id = self.metadata.get('id', '')
        self.languages = data.get('languages', [])

        self.patterns = [Pattern(pattern, self.id + index) for index, pattern in enumerate(data.get('patterns', []))]
        self.helper_patterns = [HelperPattern(helper_pattern) for helper_pattern in data.get('helper-patterns', [])]

        self.severity = self.metadata.get('severity', '')
        self.description = self.metadata.get('description', '')
        self.message = self.metadata.get('message', '')


    def __str__(self):
        return f"Rule: {self.metadata.get('name')}"

# Example rule data
rule_data = {
    'patterns': [
        {
            'pattern': "$<MODULE>($<SECRET_IN_HASH>)",
            'filters': [
                {'variable': 'MODULE', 'detection': 'another_rule_id_1'},
                {'variable': 'SECRET_IN_HASH', 'detection': 'another_rule_id_2'}
            ]
        }
    ],
    'languages': ['javascript'],
    'helper-patterns': [
        {
            'id': 'another_rule_id_1',
            'patterns': [
                {'pattern': 'import $<_> from $<LIBRARY_NAME>'}
            ],
            'filters': [
                {'variable': 'LIBRARY_NAME', 'regex': 'expressjwt'}
            ]
        },
        {
            'id': 'another_rule_id_2',
            'patterns': [
                {'pattern': '{ secret: $<STRING_LITERAL> }'}
            ],
            'filters': [
                {'variable': 'STRING_LITERAL', 'detection': 'string_literal'}
            ]
        }
    ],
    'metadata': {
        'id': 'test_rule',
        'name': 'Test Rule',
        'description': 'This is a test rule',
        'severity': 'HIGH',
        'category': 'SQL Injection',
        'status': 'ACTIVE',
        'message': 'Remediation steps: https://example.com',
        'tags': ['test', 'sql', 'injection'],
        'references': [
            'https://example.com',
            'https://example.com'
        ]
    }
}

# Create an instance of the Rule class
rule = Rule(rule_data)

# Accessing rule attributes
print(rule)
print("Patterns:", rule.patterns)
print("Languages:", rule.languages)
print("Helper Patterns:", rule.helper_patterns)
print("Metadata:", rule.metadata)
