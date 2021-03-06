"""Gets index.html for the tornado webpage.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import logging
import os
import tornado.template
import tornado.web

# Tornado example gotten from: https://github.com/wildfios/Tornado-mjpeg-streamer-python.
# Combined with: https://github.com/wildfios/Tornado-mjpeg-streamer-python/issues/7.


# pylint: disable=attribute-defined-outside-init
class HtmlPageHandler(tornado.web.RequestHandler):
    """Handler for the html page of the site that is for the main page.

    Attributes:
        configs (ConfigParser): configurations of the stream.
    """
    def initialize(self, configs):
        """Give the configurations when initializing the stream handler.

        Args:
            configs (ConfigParser): configurations.
        """
        self.configs = configs

    def get(self, file_name='index.html'):
        """Gets the html page and renders it.

        When the index.html page cannot be found it will send an error template to the webclient.

        Args:
            file_name (str): html page it is getting.
        """
        # Check if page exists.
        logging.info(f'Get html file: {file_name}')

        if file_name is None:
            file_name = 'index.html'

        # Gets path of the html page.
        html_dir_path = self.configs['Main']['html_dir_path']
        index_page = os.path.join(html_dir_path, file_name)

        if os.path.exists(index_page):
            # Render it.
            self.render(index_page)
        else:
            # Page not found, generate template.
            err_tmpl = tornado.template.Template('<html> Err 404, Page {{ name }} not found</html>')
            err_html = err_tmpl.generate(name=file_name)
            logging.error(f'no index.html found at path {index_page}')
            # Send response.
            self.finish(err_html)
