"""Contrato de progresso: entregas ponderadas, nunca contagem de issues."""
from datetime import date
import re

STATES={'planned','in_progress','in_review','blocked','done','cancelled'}


def validate(data, repository=None):
    if not isinstance(data,dict) or type(data.get('schema_version')) is not int or data.get('schema_version') != 1:
        raise ValueError('schema_version deve ser 1')
    if repository and data.get('repository') != repository:
        raise ValueError('Repositório divergente')
    if not isinstance(data.get('repository'),str) or not re.fullmatch(r'[\w.-]+/[\w.-]+',data['repository']):
        raise ValueError('Repositório inválido')
    if type(data.get('publish')) is not bool:
        raise ValueError('publish deve ser booleano')
    name=data.get('name')
    if not isinstance(name,str) or not name.strip() or len(name)>100 or any(ord(c)<32 for c in name):
        raise ValueError('Nome inválido')
    date.fromisoformat(data['updated_at'])
    scope=data.get('scope')
    if not isinstance(scope,dict) or not scope.get('name') or type(scope.get('revision')) is not int or scope['revision']<1:
        raise ValueError('Escopo e revisão obrigatórios')
    items=data.get('milestones')
    if not isinstance(items,list) or len(items)>1000:
        raise ValueError('milestones deve ser lista com até 1000 itens')
    ids=set()
    for item in items:
        if not isinstance(item,dict) or not isinstance(item.get('id'),str) or not item['id'] or item['id'] in ids:
            raise ValueError('ID ausente ou duplicado')
        ids.add(item['id'])
        if item.get('state') not in STATES or type(item.get('weight')) is not int or not 1<=item['weight']<=1000:
            raise ValueError('Estado ou peso inválido')
        evidence=item.get('evidence',[])
        if not isinstance(evidence,list) or any(not isinstance(e,str) or not e.strip() for e in evidence):
            raise ValueError('Evidência inválida')
        if item['state']=='done' and not evidence:
            raise ValueError('Entrega concluída exige evidência')
    return data


def progress(data):
    validate(data)
    items=[i for i in data['milestones'] if i['state']!='cancelled']
    total=sum(i['weight'] for i in items)
    done=sum(i['weight'] for i in items if i['state']=='done')
    return 100*done//total if total else 0


def record(data):
    validate(data)
    items=[i for i in data['milestones'] if i['state']!='cancelled']
    count=sum(i['state']=='done' for i in items)
    label=f'Entregas: {count}/{len(items)}' if items else 'Base a definir'
    return {'name':data['name'],'percent':progress(data),'status':label}


if __name__ == '__main__':
    import json
    import sys
    for filename in sys.argv[1:] or ['PROJECT_STATUS.json']:
        data=validate(json.loads(__import__('pathlib').Path(filename).read_text(encoding='utf-8')))
        print(f"{filename}: válido; {progress(data)}%")
