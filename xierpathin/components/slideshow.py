# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#   slideshow.py
#
from random import choice, shuffle
from component import Component
from xierpathin.constants import Constants
from xierpathin.toolbox.transformer import TX

class SlideShow(Component):

    # Needs buildCss content in CSS file.
    # Needs global jQuery

    C = Constants

    ARROW_RIGHT = '&gt;'
    ARROW_LEFT = '&lt;'

    def __init__(self, adapter):
        self.name = self.__class__.__name__
        self.adapter = adapter

    def build(self, b):
        # @categories is a list of category names.
        # If None, answer the poster images from all articles.
        # Otherwise, answer the poster images from the articles in the defined categories.
        siteName = self.adapter.findSiteName(b.e.getFullPath())
        category = self.adapter.findActiveCategory(b.e.getFullPath())
        if category == 'home':
            category = None # Get all poster images
        b.div(class_=self.getClassName(), id="slider")
        posters = self.adapter.getPosterArticles(category)
        b.a(href="#", class_='control_next')
        self.buildArrowRight(b)
        b._a()
        b.a(href="#", class_='control_prev')
        self.buildArrowLeft(b)
        b._a()
        b.ul()
        shuffle(posters)
        for posterArticle in posters:
            posters = TX.commaSpaceString2WordList(posterArticle.poster)
            poster = choice(posters) # Select random poster image from the list.
            b.li(style="background-image:url('/%s/%s/article-%s/%s')" % \
                (siteName, posterArticle.categories[0], posterArticle.url, poster),
                onclick="parent.location='/%s/%s/article-%s/index.html'" % (siteName, posterArticle.categories[0], posterArticle.url))
            b.div(class_='slider_transparancy')
            b.div(class_='slider_text')
            b.text(posterArticle.title)
            b._div()
            b._div()
            b._li()
        b._ul()
        b._div()

        self.buildJs(b)

    def buildArrowRight(self, b):
        b.text(self.ARROW_RIGHT)

    def buildArrowLeft(self, b):
        b.text(self.ARROW_LEFT)

    def buildJs(self, b):

        # Needs jQuery to be loaded in the page.
        b.script()
        b.text("""
jQuery(document).ready(function ($) {

    $('#checkbox').change(function(){
    setInterval(function () {
        moveRight();
    }, 3000);
    });

    var slideCount = $('#slider ul li').length;
    var slideWidth = $('#slider ul li').width();
    var slideHeight = $('#slider ul li').height();
    var sliderUlWidth = slideCount * slideWidth;

    $('#slider').css({ width: slideWidth, height: slideHeight });

    $('#slider ul').css({ width: sliderUlWidth, marginLeft: - slideWidth });

    $('#slider ul li:last-child').prependTo('#slider ul');

    function moveLeft() {
        $('#slider ul').animate({
            left: + slideWidth
        }, 200, function () {
            $('#slider ul li:last-child').prependTo('#slider ul');
            $('#slider ul').css('left', '');
        });
    };

    function moveRight() {
        $('#slider ul').animate({
            left: - slideWidth
        }, 200, function () {
            $('#slider ul li:first-child').appendTo('#slider ul');
            $('#slider ul').css('left', '');
        });
    };

    $('a.control_prev').click(function () {
        moveLeft();
    });

    $('a.control_next').click(function () {
        moveRight();
    });

});
        """)
        b._script()

    def buildCss(self, b):
        return """
            #slider {
              position: relative;
              overflow: hidden;
              margin: 20px auto 0 auto;
              border-radius: 4px;
            }

            #slider ul {
              position: relative;
              margin: 0;
              padding: 0;
              height: 200px;
              list-style: none;
            }

            #slider ul li {
              position: relative;
              display: block;
              float: left;
              margin: 0;
              padding: 0;
              width: 920px;
              height: 600px;
              background: #ccc;
              text-align: center;
              line-height: 300px;
            }

            a.control_prev, a.control_next {
              position: absolute;
              top: 40%;
              z-index: 999;
              display: block;
              padding: 4% 3%;
              width: auto;
              height: auto;
              background: #2a2a2a;
              color: #fff;
              text-decoration: none;
              font-weight: 600;
              font-size: 18px;
              opacity: 0.8;
              cursor: pointer;
            }

            a.control_prev:hover, a.control_next:hover {
              opacity: 1;
              -webkit-transition: all 0.2s ease;
            }

            a.control_prev {
              border-radius: 0 2px 2px 0;
            }

            a.control_next {
              right: 0;
              border-radius: 2px 0 0 2px;
            }

            .slider_option {
              position: relative;
              margin: 10px auto;
              width: 160px;
              font-size: 18px;
            }
        """
