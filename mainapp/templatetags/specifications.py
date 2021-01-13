from django import template
from django.utils.safestring import mark_safe

from mainapp.models import Smartphone
register = template.Library()


# tutaj generujemy wlasnie "pliki" html
TABLE_HEAD = """
            <table class="table">
                <tbody>
             """

TABLE_TAIL = """
                </tbody>
            </table>
             """

TABLE_CONTENT = """
                <tr>
                    <td>{name}</td>
                    <td>{value}</td>
                </tr>
                 """

PRODUCT_SPEC = {
    # nazwa modeli
    'notebook': {
        'Diagonal': 'diagonal',
        'Type of display': 'display',
        'CPU Frequency': 'processor_freq',
        'RAM': 'ram',
        'GPU': 'video',
        'Battery life': 'time_without_charge',
    },
    # nazwa modeli
    'smartphone': {
        'Diagonal': 'diagonal',
        'Type of display': 'display',
        'Resolution': 'resolution',
        'Battery volume': 'accum_volume',
        'RAM': 'ram',
        'SD': 'sd',
        'Maximum Embedded Memory': 'sd_volume_max',
        'Main camera': 'main_cam_mp',
        'Frontal camera': 'frontal_cam_mp'
    }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    # sprawdzamy, czy jest SD, a następnie w razie gdy niema usuwamy 'maksymalne pole pamięci'
    if isinstance(product, Smartphone):
        if not product.sd:
            PRODUCT_SPEC['smartphone'].pop('Maximum Embedded Memory')
        else:
            PRODUCT_SPEC['smartphone']['Maximum Embedded Memory'] = 'sd_volume_max'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)
