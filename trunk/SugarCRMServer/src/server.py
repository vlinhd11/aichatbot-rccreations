'''
Created on Aug 5, 2009
Created using Python 2.5
@author: Rakesh

This program is starts a server on port 8000.
This program also defines a method called "bot" and exposes as a service to the WSGI Handler.
The Bot service makes use of PyAIML library and interacts with the AIML files defined in the Sugar CRM knowledgebase
to find the appropriate responses for the questions asked by the user.
'''

#importing PyAIML library
import aiml
import os.path

# Echo Service : for testing purposes ~ Returns what ever it gets as input
def echo(data):
    """
    Just return data back to the client.
    """
    return data

#Sugar CRM Bot Service : Interacts with Sugar CRM AIML Knowledgebase and finds the appropriate response to the
#questions asked by the user and then returns it.
def bot(data):
    k = aiml.Kernel()
    if os.path.isfile("standard.brn"):
        k.bootstrap(brainFile = "standard.brn")
    else:
        k.bootstrap(learnFiles = "startup.xml", commands = "load aiml b")
        k.saveBrain("standard.brn")
    return k.respond(data)

#Services defined
services = {
    'echo': echo,
    'bot' : bot
}

if __name__ == '__main__':

    #Importing PyAMF library
    import os
    from pyamf.remoting.gateway.wsgi import WSGIGateway
    from wsgiref import simple_server

    gw = WSGIGateway(services)

    httpd = simple_server.WSGIServer(
        ('localhost', 8000),
        simple_server.WSGIRequestHandler,
    )

    def app(environ, start_response):
        if environ['PATH_INFO'] == '/crossdomain.xml':
            fn = os.path.join(os.getcwd(), os.path.dirname(__file__),
               'crossdomain.xml')

            fp = open(fn, 'rt')
            buffer = fp.readlines()
            fp.close()

            start_response('200 OK', [
                ('Content-Type', 'application/xml'),
                ('Content-Length', str(len(''.join(buffer))))
            ])

            return buffer

        return gw(environ, start_response)

    httpd.set_app(app)

    print "Running Sugar CRM AMF gateway on http://localhost:8000"

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


