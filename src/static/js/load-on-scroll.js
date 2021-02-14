$(document).ready(function() {
    
    function getNewAdListItem(image_src, price, title){
        const $newNode = $('.ad-list-item__wrapper').last().clone(true);

        $newNode.find('.ad-list__item_pic img').attr('src', image_src);
        $newNode.find('.ad-ad-list__item__price').text(price);
        $newNode.find('.ad-ad-list__item__title').text(title);

        return $newNode;
    }

    function constructAdList(data, container) {
        const adList = [];
        const dataLen = data.length;
        for(let i=0; i < dataLen; ++i) {
            const $newAdElem = getNewAdListItem(
                image_src = data[i].image_src,
                price = data[i].price,
                title = data[i].price
            )
            $(container).append($newAdElem);
        }
    }
    
    const data = [
        {
            'image_src': '/static/images/subaru.jpeg',
            'price': '123$',
            'title':'Temporary'
        },
        {
            'image_src': '/static/images/subaru.jpeg',
            'price': '123$',
            'title':'Temporary'
        },
        {
            'image_src': '/static/images/subaru.jpeg',
            'price': '123$',
            'title':'Temporary'
        },
        {
            'image_src': '/static/images/subaru.jpeg',
            'price': '123$',
            'title':'Temporary'
        },
    ]

    $(window).scroll(function() {

        if($(window).scrollTop() + $(window).height() >= $(document).height()){
            const $adListContainer = $('.ad-list-container');

            // get data with ajax

            constructAdList(data, $adListContainer);
        }
    });

});