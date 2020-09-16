from mitmproxy import ctx

from satellite.vault.transformer import transformer_map


def transform_body(route, content):
    content_rewrite = ''
    for rule_entry in route.rule_entries_list:
        transformer = rule_entry.transformer
        transformer_type = transformer_map.get(transformer)
        if not transformer_type:
            ctx.log.info(f'{transformer} can\'t be used as a transformer. '
                         f'Possible values: {str(transformer_map.keys())}')
            continue
        operation = rule_entry.operation
        token_generator = rule_entry.public_token_generator
        transformer_config = rule_entry.transformer_config
        content_rewrite = transformer_type.transform(content, transformer_config, token_generator, operation)
    return content_rewrite
