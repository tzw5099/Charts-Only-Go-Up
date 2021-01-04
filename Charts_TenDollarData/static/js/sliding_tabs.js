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
			.attr("id", "tab-" + i)
			.addClass("tab")
			.wrapInner("<div class='tab-wrapper'></div>");
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
			.attr("id", "panel-" + i)
			.addClass("panel")
			.wrapInner("<div class='panel-wrapper'></div>")
			.prepend("<div class='accordion-tab'></div>");
	});
$(".accordion-tab").each(function (i) {
	i = i + 1;
	var tab_name = $("#tab-" + i).html();
	$(this).html(tab_name);
});
$("#qaz_tabs").children().eq(selectedTab).addClass("xactive");
$("#qaz_panels").children().eq(selectedTab).addClass("xactive");
$("#qaz_tabs > li").click(function () {
	$("#qaz_tabs > li, #qaz_panels > li").removeClass("xactive");
	$("#qaz_panels > li").eq($(this).index()).toggleClass("xactive");
	$(this).toggleClass("xactive");
});
$(".accordion-tab").click(function () {
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
			.attr("id", "tab-" + i)
			.addClass("tab")
			.wrapInner("<div class='tab-wrapper'></div>");
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
			.attr("id", "panel-" + i)
			.addClass("panel")
			.wrapInner("<div class='panel-wrapper'></div>")
			.prepend("<div class='accordion-tab'></div>");
	});
$(".accordion-tab").each(function (i) {
	i = i + 1;
	var tab_name = $("#tab-" + i).html();
	$(this).html(tab_name);
});
$("#wsx_tabs").children().eq(selectedTab).addClass("xactive");
$("#wsx_panels").children().eq(selectedTab).addClass("xactive");
$("#wsx_tabs > li").click(function () {
	$("#wsx_tabs > li, #wsx_panels > li").removeClass("xactive");
	$("#wsx_panels > li").eq($(this).index()).toggleClass("xactive");
	$(this).toggleClass("xactive");
});
$(".accordion-tab").click(function () {
	$("#wsx_tabs > li, #wsx_panels > li").removeClass("xactive");
	$("#wsx_tabs > li").eq($(this).parent().index()).toggleClass("xactive");
	$(this).parent().toggleClass("xactive");
});

// jQuery Responsive edcpage edctabs 1.0
var selectedTab = 0,
	scrollDelay = 20,
	scrollSpeed = 400,
	scrolltopOffset = 0;

$("#edctabs")
	.children()
	.each(function (i) {
		i = i + 1;
		$(this)
			.attr("id", "tab-" + i)
			.addClass("tab")
			.wrapInner("<div class='tab-wrapper'></div>");
	});
var count = $("#edctabs").children().length - 1;
var tab_width = 100 / count + "%";
$("#edctabs li")
	.css("width", tab_width)
	.eq(0)
	.addClass("first")
	.end()
	.eq(-1)
	.addClass("last")
	.end();
$("#edcpanels")
	.children()
	.each(function (i) {
		i = i + 1;
		$(this)
			.attr("id", "panel-" + i)
			.addClass("panel")
			.wrapInner("<div class='panel-wrapper'></div>")
			.prepend("<div class='accordion-tab'></div>");
	});
$(".accordion-tab").each(function (i) {
	i = i + 1;
	var tab_name = $("#tab-" + i).html();
	$(this).html(tab_name);
});
$("#edctabs").children().eq(selectedTab).addClass("xactive");
$("#edcpanels").children().eq(selectedTab).addClass("xactive");
$("#edctabs > li").click(function () {
	$("#edctabs > li, #edcpanels > li").removeClass("xactive");
	$("#edcpanels > li").eq($(this).index()).toggleClass("xactive");
	$(this).toggleClass("xactive");
});
$(".accordion-tab").click(function () {
	$("#edctabs > li, #edcpanels > li").removeClass("xactive");
	$("#edctabs > li").eq($(this).parent().index()).toggleClass("xactive");
	$(this).parent().toggleClass("xactive");
});
