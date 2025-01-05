from django.template import Template, Context
from django.test import TestCase


class ProductInfoTemplateTests(TestCase):
    def render_template(self, context_data):
        """
        Helper function to render the template snippet with the given context.
        """
        template_code = """
        <p class="my-0"><strong>{{ item.product.name }}</strong></p>
        <p class="my-0">
            <strong>Size: </strong>
            {% if item.product.has_sizes %}
                {{ item.size|upper }}
            {% else %}
                N/A
            {% endif %}
        </p>
        <p class="my-0 small text-muted">SKU: {{ item.product.sku|upper }}</p>
        """
        template = Template(template_code)
        return template.render(Context(context_data))

    def test_product_info_with_size(self):
        """
        Test rendering of product information when the product has sizes.
        """
        context = {
            "item": {
                "product": {
                    "name": "Test Product",
                    "has_sizes": True,
                    "sku": "abc123",
                },
                "size": "m",
            }
        }
        rendered = self.render_template(context)

        self.assertIn("<strong>Test Product</strong>", rendered)
        self.assertIn("<strong>Size: </strong>M", rendered)
        self.assertIn("SKU: ABC123", rendered)

    def test_product_info_without_size(self):
        """
        Test rendering of product information when the product does not have sizes.
        """
        context = {
            "item": {
                "product": {
                    "name": "Another Product",
                    "has_sizes": False,
                    "sku": "xyz789",
                },
                "size": "",
            }
        }
        rendered = self.render_template(context)

        self.assertIn("<strong>Another Product</strong>", rendered)
        self.assertIn("<strong>Size: </strong>N/A", rendered)
        self.assertIn("SKU: XYZ789", rendered)