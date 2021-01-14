// jQuery Responsive qaz_page qaz_tabs 1.0
// $("body").css("overflow", "hidden");
var selectedTab = 0,
	scrollDelay = 20,
	scrollSpeed = 400,
	scrolltopOffset = 0;

$("#qaz_tabs")
	.children()
	.each(function (i) {
		i = i + 1;
		$(this)
			.attr("id", "qaz_tab-" + i)
			.addClass("qaz_tab")
			.wrapInner("<div class='qaz_tab-wrapper'></div>");
	});
var count = $("#qaz_tabs").children().length - 1;
var tab_width = 100 / count + "%";
$("#qaz_tabs li")
	.css("width", tab_width)
	.eq(0)
	.addClass("first")
	.end()
	.eq(-1)
	.addClass("last")
	.end();
$("#qaz_panels")
	.children()
	.each(function (i) {
		i = i + 1;
		$(this)
			.attr("id", "qaz_panel-" + i)
			.addClass("qaz_panel")
			.wrapInner("<div class='qaz_panel-wrapper'></div>")
			.prepend("<div class='qaz_accordion-tab'></div>");
	});
$(".qaz_accordion-tab").each(function (i) {
	i = i + 1;
	var tab_name = $("#qaz_tab-" + i).html();
	$(this).html(tab_name);
});
$("#qaz_tabs").children().eq(selectedTab).addClass("xactive");
$("#qaz_panels").children().eq(selectedTab).addClass("xactive");
$("#qaz_tabs > li").click(function () {
	$("#qaz_tabs > li, #qaz_panels > li").removeClass("xactive");
	$("#qaz_panels > li").eq($(this).index()).toggleClass("xactive");
	$(this).toggleClass("xactive");
});
$(".qaz_accordion-tab").click(function () {
	$("#qaz_tabs > li, #qaz_panels > li").removeClass("xactive");
	$("#qaz_tabs > li").eq($(this).parent().index()).toggleClass("xactive");
	$(this).parent().toggleClass("xactive");
});

// jQuery Responsive wsx_page wsx_tabs 1.0

var selectedTab = 0,
	scrollDelay = 20,
	scrollSpeed = 400,
	scrolltopOffset = 0;

$("#wsx_tabs")
	.children()
	.each(function (i) {
		i = i + 1;
		$(this)
			.attr("id", "wsx_tab-" + i)
			.addClass("wsx_tab")
			.wrapInner("<div class='wsx_tab-wrapper'></div>");
	});
var count = $("#wsx_tabs").children().length - 1;
var tab_width = 100 / count + "%";
$("#wsx_tabs li")
	.css("width", tab_width)
	.eq(0)
	.addClass("first")
	.end()
	.eq(-1)
	.addClass("last")
	.end();
$("#wsx_panels")
	.children()
	.each(function (i) {
		i = i + 1;
		$(this)
			.attr("id", "wsx_panel-" + i)
			.addClass("wsx_panel")
			.wrapInner("<div class='wsx_panel-wrapper'></div>")
			.prepend("<div class='wsx_accordion-tab'></div>");
	});
$(".wsx_accordion-tab").each(function (i) {
	i = i + 1;
	var tab_name = $("#wsx_tab-" + i).html();
	$(this).html(tab_name);
});
$("#wsx_tabs").children().eq(selectedTab).addClass("xactive");
$("#wsx_panels").children().eq(selectedTab).addClass("xactive");
$("#wsx_tabs > li").click(function () {
	$("#wsx_tabs > li, #wsx_panels > li").removeClass("xactive");
	$("#wsx_panels > li").eq($(this).index()).toggleClass("xactive");
	$(this).toggleClass("xactive");
});
$(".wsx_accordion-tab").click(function () {
	$("#wsx_tabs > li, #wsx_panels > li").removeClass("xactive");
	$("#wsx_tabs > li").eq($(this).parent().index()).toggleClass("xactive");
	$(this).parent().toggleClass("xactive");
});

// jQuery Responsive edc_page edc_tabs 1.0
var selectedTab = 0,
	scrollDelay = 20,
	scrollSpeed = 400,
	scrolltopOffset = 0;

$("#edc_tabs")
	.children()
	.each(function (i) {
		i = i + 1;
		$(this)
			.attr("id", "edc_tab-" + i)
			.addClass("edc_tab")
			.wrapInner("<div class='edc_tab-wrapper'></div>");
	});
var count = $("#edc_tabs").children().length - 1;
var tab_width = 100 / count + "%";
$("#edc_tabs li")
	.css("width", tab_width)
	.eq(0)
	.addClass("first")
	.end()
	.eq(-1)
	.addClass("last")
	.end();
$("#edc_panels")
	.children()
	.each(function (i) {
		i = i + 1;
		$(this)
			.attr("id", "edc_panel-" + i)
			.addClass("edc_panel")
			.wrapInner("<div class='edc_panel-wrapper'></div>")
			.prepend("<div class='edc_accordion-tab'></div>");
	});
$(".edc_accordion-tab").each(function (i) {
	i = i + 1;
	var tab_name = $("#edc_tab-" + i).html();
	$(this).html(tab_name);
});
$("#edc_tabs").children().eq(selectedTab).addClass("xactive");
$("#edc_panels").children().eq(selectedTab).addClass("xactive");
$("#edc_tabs > li").click(function () {
	$("#edc_tabs > li, #edc_panels > li").removeClass("xactive");
	$("#edc_panels > li").eq($(this).index()).toggleClass("xactive");
	$(this).toggleClass("xactive");
});
$(".edc_accordion-tab").click(function () {
	$("#edc_tabs > li, #edc_panels > li").removeClass("xactive");
	$("#edc_tabs > li").eq($(this).parent().index()).toggleClass("xactive");
	$(this).parent().toggleClass("xactive");
});
