from stitchclient.client import Client

with Client(
    192843,
    '5a10f5895e8cd98429ec9df25e00a67abd069ea689919f6f7ba99f33cbb7d4cc',
    'eu',
    callback_function=print,
    ) as client:
    for i in range(1, 10):
        client.push({
            'action': 'upsert',
            'table_name': 'test_table',
            'key_names': ['id'],
            'sequence': i,
            'data': {
                'id': i,
                'value': 'abc',
            },
        }, i)