import pygame
class Button():
    def __init__(self,image,pos,textInput,font,baseColor,hoveringColor): # button class
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.baseColor, self.hoveringColor = baseColor, hoveringColor
        self.textInput = textInput
        self.text = self.font.render(self.textInput, True, self.baseColor)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.textRect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        
    def update(self, screen):  # draw button
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.textRect)
    
    def checkForInput(self, position): # check if clicked
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColor(self, position): # change color on hover
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.textInput, True, self.hoveringColor)
        else:
            self.text = self.font.render(self.textInput, True, self.baseColor)