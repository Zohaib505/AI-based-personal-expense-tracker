from datetime import date
from django.apps import apps


def add_expense_action(amount: float, category: str, description: str = "") -> str:
    """Adds a new expense entry directly to the database."""
    try:
        Expense = apps.get_model('expenses', 'Expense')
        User = apps.get_model('auth', 'User')

        # Base kwargs for creation
        kwargs = {
            'amount': amount,
            'description': description,
            'date': date.today()
        }

        # Inspect model fields to handle foreign keys automatically
        model_fields = [f.name for f in Expense._meta.get_fields()]
        default_user = User.objects.first()

        # Handle user/owner requirement
        if 'owner' in model_fields and default_user:
            kwargs['owner'] = default_user
        elif 'user' in model_fields and default_user:
            kwargs['user'] = default_user

        # Handle category field (CharField vs ForeignKey)
        if 'category' in model_fields:
            field = Expense._meta.get_field('category')
            if field.is_relation:
                Category = field.related_model
                category_obj, _ = Category.objects.get_or_create(name=category.capitalize())
                kwargs['category'] = category_obj
            else:
                kwargs['category'] = category

        # Create the expense entry
        Expense.objects.create(**kwargs)
        return f"Successfully recorded expense of ${amount:.2f} under category '{category}'."

    except Exception as e:
        # Prints exact exception in the runserver terminal console for easy debugging
        print(f"\n[AI Chatbot Database Error]: {str(e)}\n")
        return f"Failed to record expense: {str(e)}"


def get_expense_summary_action() -> str:
    """Calculates total spending and count from existing database entries."""
    try:
        Expense = apps.get_model('expenses', 'Expense')
        expenses = Expense.objects.all()
        total = sum(e.amount for e in expenses)
        return f"Total expenses recorded: ${total:.2f} across {expenses.count()} entries."
    except Exception as e:
        print(f"\n[AI Chatbot Database Error]: {str(e)}\n")
        return f"Failed to retrieve expense summary: {str(e)}"


TOOLS = [
    {
        'type': 'function',
        'function': {
            'name': 'add_expense_action',
            'description': 'Add a new expense record when the user mentions spending money or paying for something.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'amount': {
                        'type': 'number',
                        'description': 'The numerical amount spent.',
                    },
                    'category': {
                        'type': 'string',
                        'description': 'Category of the expense (e.g., Food, Transport, Bills, Shopping, Groceries).',
                    },
                    'description': {
                        'type': 'string',
                        'description': 'Optional brief note or details about the expense.',
                    },
                },
                'required': ['amount', 'category'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_expense_summary_action',
            'description': 'Retrieve total spending details and summary from the database when asked about total expenses or balance.',
            'parameters': {
                'type': 'object',
                'properties': {},
            },
        },
    },
]

AVAILABLE_FUNCTIONS = {
    'add_expense_action': add_expense_action,
    'get_expense_summary_action': get_expense_summary_action,
}