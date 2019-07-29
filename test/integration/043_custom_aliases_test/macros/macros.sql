
{% macro generate_alias_name(custom_alias_name, node) -%}
    {%- if custom_alias_name is none -%}
        {{ node.name }}
    {%- else -%}
        custom_{{ custom_alias_name | trim }}
    {%- endif -%}
{%- endmacro %}


{% macro string_literal(s) -%}
  {{ adapter_macro('test.string_literal', s) }}
{%- endmacro %}

{% macro default__string_literal(s) %}
    '{{ s }}'::text
{% endmacro %}

{% macro bigquery__string_literal(s) %}
    cast('{{ s }}' as string)
{% endmacro %}
