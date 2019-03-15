var app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#app',
  data: {
    queue: {"items": [], "size": []},
    cart: {"items": [], "size": []},
    returns: {"items": [], "size": []},
  },
  created: function () {
    this.fetchData()
  },
  methods: {
    fetchData: function () {
      var xhr = new XMLHttpRequest()
      var self = this
      xhr.open('GET', '/api/containers.json')
      xhr.onload = function () {
        self.queue.items = JSON.parse(xhr.responseText)
        self.updateSize()
      }
      xhr.send()
    },
    updateSize: function() {
      var self = this
      var l
      var lists = [this.queue, this.cart, this.returns]
      for (l in lists) {
        var x
        var size = 0
        var list = lists[l]
        for (x in list.items) {
          var element = list.items[x]
          size += parseFloat((element.width*element.height*element.depth)/1728)
        }
        list.size = size.toFixed(2)
      }
    },
    checkSize: function(evt) {
      if (evt.to.className=='list-group cart'&&(parseFloat(this.cart.size) +
           parseFloat(evt.draggedContext.element.height*evt.draggedContext.element.width*evt.draggedContext.element.depth/1728)) > 2) {
        return false
      }
    }
  }
});
