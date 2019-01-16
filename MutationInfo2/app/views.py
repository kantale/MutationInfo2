from django.shortcuts import render
from django.http import HttpResponse

import re
import simplejson


def index(request):
    context = {}
    create_regular_expression()
    return render(request, 'app/index.html', {})

def has_data(f):
    '''
    Decorator that passes AJAX data to a function parameters
    '''
    def wrapper(*args, **kwargs):
            request = args[0]
            if request.method == 'POST':
                    if len(request.POST):
                            for k in request.POST:
                                    kwargs[k] = request.POST[k]
                    else:
                            POST = simplejson.loads(request.body)
                            for k in POST:
                                    kwargs[k] = POST[k]
            elif request.method == 'GET':
                    for k in request.GET:
                            kwargs[k] = request.GET[k]
                            print ("GET: {} == {}".format(k, kwargs[k]))

            return f(*args, **kwargs)

    return wrapper


def create_regular_expression():
    '''
    refseq = r'NM_[\d]+\.[\d]+|NM_[\d]+'
    ensembl = r'ENST[\d]+\.[\d]+|ENST[\d]+'
    chromosome = r'1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|x|y|X|Y'
    transcript = r'(?P<refseq>{})|(?P<ensembl>{})|(?P<gene>[\w]+)|(?P<hgvs_chromosome>{})'.format(refseq, ensembl, chromosome)

    We do not allow multiple alternatives
    1387C->T/A

    NT_005120.15:c.1160CC>GT -->  NT_005120.15(UGT1A1):c.1160_1161delinsGT  
    '''

    def correct_hgvs(transcript, coord_type, start_position, end_position, reference_sequence, alternative_sequence, ref_alt_sep):
        if len(reference_sequence) == len(alternative_sequence) and len(reference_sequence)>1:
            # NT_005120.15:c.1160CC>GT -->  NT_005120.15:c.1160_1161delinsGT  
            end_position = int(start_position) + len(reference_sequence) - 1
            end_position = f'_{end_position}'
            return f'{transcript}:{coord_type}{start_position}{end_position}delins{alternative_sequence}'

        if not end_position:
            return f'{transcript}:{coord_type}{start_position}{reference_sequence}>{alternative_sequence}'
        

    transcript = r'(?P<transcript>[\w\.]+)'
    coord_type = r'(?P<coord_type>c\.|g\.)'
    start_position = r'(?P<start_position>-?[\d]+)' # -100
    end_position = r'(?P<end_position>_-?[\d]+)' # _100
    reference_sequence = r'(?P<reference_sequence>[ACGT]+)' # ACGT
    alternative_sequence = r'(?P<alternative_sequence>[ACGT]+)' # ACGT
    ref_alt_sep = r'(?P<ref_alt_sep>-?>)'  # >, ->

    hgvs_snp_re = rf'{transcript}:{coord_type}{start_position}({end_position})?\(?{reference_sequence}{ref_alt_sep}{alternative_sequence}\)?'



    tests = [
        'NM_123423.3:c.231A>G',
        'NM_123423.3:c.231A->G',
        'NM_123423.3:c.231(A->G)',
        'NT_005120.15:c.1160CC>GT',
    ]

    for test in tests:
        m = re.match(hgvs_snp_re, test)
        d = m.groupdict()
        hgvs_s = correct_hgvs(**d)
        print (hgvs_s)


@has_data
def answer(request, **kwargs):
    question = kwargs['question']

    json = simplejson.dumps({"reply": 'testtt'})
    return HttpResponse(json, content_type='application/json')
