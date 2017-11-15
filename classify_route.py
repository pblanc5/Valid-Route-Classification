import datetime
import jinja2
import getpass
import nltk
import pickle
import sys
import os

def get_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [line for line in lines]

def find_features(document):
    word_features = pickle.load(open("Util/word_features.pickle", "rb"))
    words = nltk.word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features


def classify_routes(routes):
    classifier = pickle.load(open("Classifiers/SGD_classifier.pickle", "rb"))
    items = []
    for route in routes:
        features = find_features(route)
        items.append({'ip':route.split()[3], "class":classifier.classify(features), "output":route})
    return items

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

def render_report(items):
    title = getpass.getuser() + '\'s Routing Report ' + f"{datetime.datetime.now():%Y-%m-%d %H:%M}"
    context = {
        "title":title,
        "items":items,
    }

    res = render("Templates/template_report.jinja2", context)
    res_f = open(title+'.html', 'w')
    res_f.write(res)
    res_f.close()

if __name__ == "__main__":
    filename = sys.argv[1]
    routes = get_input(filename)
    items = classify_routes(routes)
    render_report(items)
