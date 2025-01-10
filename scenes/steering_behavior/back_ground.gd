extends ColorRect

var r: float = 0.0
var g: float = 0.0
var b: float = 0.0
var r_next: float
var g_next: float
var b_next: float
const NEXT = 0.01


func _ready() -> void:
	r_next = NEXT
	g_next = NEXT
	b_next = NEXT

func _process(delta: float) -> void:
	calc_color()

func calc_color():
	
	b += b_next
	
	if b >= 1.0 - NEXT:
		b_next = -NEXT
	if b <= 0 + NEXT:
		b_next = NEXT
		g += g_next
		if g >= 1.0 - NEXT:
			g_next = -NEXT
		if g <= 0 + NEXT:
			g_next = NEXT
			r += r_next
			if r >= 1.0 - NEXT:
				r_next = -NEXT
			if r <= 0 + NEXT:
				r_next = NEXT
	
	print(r, " ", g, " ", b, " ")
		
	color = Color(r, g, b)
