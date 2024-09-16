extends Camera2D


var _screen_width: int
var _screen_height: int

var _scroll_left: bool = false
var _scroll_right: bool = false
var _scroll_up:bool = false
var _scroll_down:bool = false
var _scroll_speed:int = 200

var _zooming:Vector2 = Vector2(0.0, 0.0)
var _zoom_speed: int = 10

var _focus: bool = true


func _ready():
	_screen_width = get_viewport().size.x
	_screen_height = get_viewport().size.y
	get_viewport().size_changed.connect(self._resize)


func _notification(what):
	if what == NOTIFICATION_WM_MOUSE_ENTER:
		_focus = true
	if what == NOTIFICATION_WM_MOUSE_EXIT:
		_focus = false


func _process(delta):
	_scroll_left = false
	_scroll_right = false
	_scroll_up = false
	_scroll_down = false
		
	var m_x = get_viewport().get_mouse_position().x
	var m_y = get_viewport().get_mouse_position().y

	if m_x < 5:
		_scroll_left = true
	if m_x > _screen_width - 5:
		_scroll_right = true
	if m_y < 5:
		_scroll_up = true
	if m_y > _screen_height - 5:
		_scroll_down = true

	if _focus:
		_scroll(delta)
		_zoom(delta)
		_zooming = Vector2(0.0, 0.0)


func _input(event):
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			_zooming = Vector2(1, 1)
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			_zooming = Vector2(-1, -1)


func _scroll(delta):
	if _scroll_left:
		position.x -= _scroll_speed * delta
	
	if _scroll_right:
		position.x += _scroll_speed * delta
		
	if _scroll_up:
		position.y -= _scroll_speed * delta
		
	if _scroll_down:
		position.y += _scroll_speed * delta


func _zoom(delta):
	zoom += _zooming * _zoom_speed * delta


func _resize():
	_screen_width = get_viewport().size.x
	_screen_height = get_viewport().size.y
