import math

def dict_and_docs(fnames):
    simbolos_a_blancos = ".,;:()[]{}*-\"\\/+_"
    simbolos_a_eliminar = "'1234567890-?@!"
    s = set()
    docs  =[]
    for l in fnames:
        words = open("archivos_ninios/"+l).read()
        words = words.lower()
        for c in simbolos_a_blancos:
            words = words.replace(c, " ")
        for c in simbolos_a_eliminar:
            words = words.replace(c, "")
        words = words.split() 
        docs.append(words)

        for w in words:
            s.add(w)
    return (s,docs)


def vectorentropy(v):
    entropy = 0
    total = 0
    for i in v:
        total += i
    for i in v:
        if(total > 0):
            pi = i/total
            if pi > 0:
                entropy += pi*math.log2(pi)
    return -1*entropy


def nfvector(w,docs):
        return [ d.count(w)/len(d) for d in docs]
    
    
def wordsbyrelevance(dict, docs):  
    tuples  = []
    for w in dict:
        v = nfvector(w, docs)
        ne = vectorentropy(v)/math.log2(len(docs))
        tuples.append((ne,w))
    tuples.sort()
    return tuples


def project_vect(v, dimlist):
    return [v[d] for d in dimlist]


def normvect(v):
    norm = 0
    for x in v:
        norm += x*x
    norm = math.sqrt(norm)
    div = norm
    if norm == 0:
        div = 1
        
    return [x/div for x in v]


def mkvect(weights, coordinates):
    assert len(weights) == len(coordinates)
    v = [0]*len(dict)
    for i in range(len(weights)):
        v[coordinates[i]] = weights[i]
    return v


def vectadd(v1, v2):
    assert len(v1) == len(v2)
    v = [0]*len(v1)
    for i in range(len(v1)):
        v[i] = v1[i] + v2[i]
    return v

    
def vectdot(v1,v2):
    assert len(v1) == len(v2)
    res = 0
    for i in range(len(v1)):
        res += v1[i]*v2[i]
    return res


def wordcos(w1,w2):
    return vectdot(vectors[dictinv[w1]],vectors[dictinv[w2]])


def vectminus(v1,v2):
    assert len(v1) == len(v2)
    res = [0]*len(v1)
    for i in range(len(v1)):
        res[i] = v1[i] - v2[i]
    return res


def bydistance(word):
    dw = [(wordcos(word,other),other) for other in dict]
    dw.sort()
    dw.reverse()
    dwq = [w for (r,w) in dw]
    return dwq


def pairs_distance(t1,t2):
    w1, w2 = t1
    w3, w4 = t2
    w1, w2 = vectors[dictinv[w1]], vectors[dictinv[w2]]
    w3, w4 = vectors[dictinv[w3]], vectors[dictinv[w4]]
    v1 = normvect(vectminus(w1,w2))
    v2 = normvect(vectminus(w3,w4))
    return vectdot(v1,v2)


lines = open("archivos_ninios/archivos.txt").read().split()
dict, docs = dict_and_docs(lines)
dict = list(dict)
dictinv = {}
for i in range(len(dict)):
    dictinv[dict[i]] = i

intdocs = [[dictinv[w] for w in d] for d in docs]
   
wr =wordsbyrelevance(dict,docs)
wr = [(r,w) for (r,w) in wr if r >0]
wr = wr[:512]
most_relevant_words = [w for (r,w) in wr]
most_relevant_words
most_relevant_words_idxs = [dictinv[w] for w in most_relevant_words]
most_relevant_words_idxs.sort()
dimlist = most_relevant_words_idxs

weights_vectorB = [0.02777777777777779, 0.05555555555555556, 0.08333333333333333, 0.11111111111111112, 0.1388888888888889, 0.16666666666666666]
weights_vectorF = [0.16666666666666666, 0.1388888888888889, 0.11111111111111112, 0.08333333333333333, 0.05555555555555556, 0.02777777777777779]
##weights_vector = [0.0075, 0.015, 0.03, 0.06, 0.125, 0.2625*2, .125,.06,.03,.015,.0075]

#print (most_relevant_words);

vectors = [[0.0]*len(dict)]* len(dict)

vectorsBack = [[0.0]*len(dict)]* len(dict)
vectorsForward = [[0.0]*len(dict)]* len(dict)
nocurrences = [0]*len(dict)
vectors = [[x/max(1,nocurrences[i]) for x in vectors[i]] for i in range(len(vectors))]    

for d in intdocs:
    offset = len(weights_vectorB)-1
    nwords = len(d)
    for i in range(offset, nwords-offset):
        vectorsBack[d[i]] = vectadd(vectorsBack[d[i]], mkvect(weights_vectorB, d[i-offset:i+1]))
        vectorsForward[d[i]] = vectadd(vectorsForward[d[i]], mkvect(weights_vectorF, d[i:i+offset+1]))
        nocurrences[d[i]] += 1
        
for i in range(len(vectors)):
    vectors[i] = project_vect(vectorsBack[i],dimlist)+project_vect(vectorsForward[i],dimlist)
    vectors[i] = normvect(vectors[i])
print(bydistance("horse"))

#print (pairs_distance(("christmas","eve"), ("horse", "riding")))
