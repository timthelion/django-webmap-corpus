@DjangoWebmap = {} # Application namespace

class JsonStorage
	###
	Provides getting and setting JSON-serialized objects in localStorage,
	which otherwise supports key-value strings storage only.
	###
	constructor: (namespace) ->
		if Storage?
			storage = localStorage

			@getObject = (name) ->
				data = storage.getItem(namespace)
				if data then JSON.parse(data)[name] else null

			@setObject = (name, val) ->
				data = storage.getItem(namespace)
				data = if data then JSON.parse(data) else {}
				data[name] = val
				storage.setItem namespace, JSON.stringify data

		else
			@getObject = @setObject = -> null


@DjangoWebmap.storage = new JsonStorage('webmap')


# Enhance strings with truncete method.
String::truncate = (n) ->
	@substr(0, n - 1).trim() + ((if @length > n then "&hellip;" else ""))


$.fn.fillViewport = ->
	###
	jQuery plugin for stretching an element height to fill down the browser window
	###
	$window = $(window)
	$elem = this
	$nano = $('.nano')

	$window.resize ->
		$userInfoHeight = $('#user-info').innerHeight()
		$contentHeight = $(window).height() - $userInfoHeight
		$kindListHeight = $('.kinds-list').height()

		# fill up the vertical space with the map
		$elem.css 'min-height', "#{ Math.max $window.outerHeight() - $userInfoHeight, 320 }px"

		$('.gold').css('min-height', $contentHeight + 'px')
		# for all nanos outside filter
		if not $nano.parents('.filter') or $contentHeight < $kindListHeight
			$nano.css('min-height', $contentHeight + 'px')
			$nano.css({'max-height': $contentHeight + 'px'})
		# for nano in filter and only if the content height is higher than the filter content
		else if $kindListHeight != null
			$nano.css('min-height', ( $kindListHeight + 50) + 'px')
			$nano.css({'max-height': ( $kindListHeight + 50) + 'px'})
		# normal "full" height
		else
			$nano.css('min-height', ( $contentHeight) + 'px')
			$nano.css({'max-height': ( $contentHeight) + 'px'})

		$nano.nanoScroller()
	.trigger 'resize'
