var __main = function() {
    content = document.querySelector('.hidden-content').innerText
    console.log(content, marked(content))
    document.querySelector('#topic-content').innerHTML = marked(content)
}

__main()
