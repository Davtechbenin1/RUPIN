#Coding:utf-8
import time
def _on_req_close(self,*args,**kwargs):
	if list(self._modal_surf_list):
		modal = self._modal_surf_list[-1]
		self._modal_surf_list.remove(modal)
		modal.dismiss()
		return True

	curent_show = self.ps_m.menu_in_action
	if curent_show.lower() == self.ps_m.close_menu.lower():
		return False
	else:
		self.ps_m.menu_in_action = self.ps_m.close_menu
		t = time.time()
		self.ps_m.mother._action_but_(self.ps_m.close_menu)
	return True

def on_key_down(self, window, key, scancode, codepoint, modifiers):
	# 13 = ENTER
	if key == 13:
		self.dispatch_default_button()
	#if key == 27:
	#	self._on_req_close()
	
def set_default_button(self, btn):
	self.default_button = btn

def dispatch_default_button(self):
	if self.default_button and self.default_button.disabled is False:
		self.default_button.trigger_action()
		self.default_button = None

