function swapElements(elm1, elm2) {
    var parent1, parent2;

    parent1 = elm1.parent();
    parent2 = elm2.parent();

    parent1.append(elm2);
    parent2.append(elm1);
}

jq(document).ready(function() {
    // var my_url = document.baseURI;
    // // var portal_url = "http://"+document.domain;
    // 
    // // swap feeditem with newsitem right top
    // var feeditem, newsitem;
    // feeditem = jq(".FeedFeederItem").first()
    // newsitem = jq(".newsitem01");
    // if (feeditem && !feeditem.hasClass("newsitem01")) {
    //     swapElements(feeditem, newsitem);
    //     feeditem.addClass("teaserLastRowItem");
    //     newsitem.removeClass("teaserLastRowItem");
    // }

});




