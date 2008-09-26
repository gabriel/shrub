from id3 import id3reader

class ID3Data:
  """Behaves like a file so ID3Reader can process data we get from other sources."""  
  
  def __init__(self, content):
    self.content = content
    self.buffer = StringBuffer(content)
  
  def read(self, size):
    return self.buffer.read(size)
  
  def seek(self, offset, whence):
    if whence == 1:
      self.buffer.read(offset)
    if whence == 2:      
      # jump_offset = len(self.content) + offset
      # self.buffer = StringBuffer(self.content)
      # self.buffer.read(jump_offset)
      raise id3reader.Id3Error('Trying to search from the end')
    
  def close(self):
    pass

# To allow our data to be read and seekable we wrap the string in a 
# StringBuffer, defined below
# 
# This was taken from: http://coding.derkeiler.com/Archive/Python/comp.lang.python/2004-06/2524.html

class Deque: 
  """A double-ended queue.""" 
  
  def __init__(self): 
    self.a = [] 
    self.b = [] 
    
  def push_last(self, obj): 
    self.b.append(obj) 
    
  def push_first(self, obj): 
    self.a.append(obj) 
    
  def partition(self): 
    if len(self) > 1: 
      self.a.reverse() 
      all = self.a + self.b 
      n = len(all) / 2 
      self.a = all[:n] 
      self.b = all[n:] 
      self.a.reverse() 
      
  def pop_last(self): 
    if not self.b: self.partition() 
    try: return self.b.pop() 
    except: return self.a.pop() 
    
  def pop_first(self): 
    if not self.a: self.partition() 
    try: return self.a.pop() 
    except: return self.b.pop() 
    
  def __len__(self): 
    return len(self.b) + len(self.a) 
    
    
class StringBuffer(Deque): 
  """A FIFO for characters. Strings can be efficiently 
     appended to the end, and read from the beginning. 
     Example: 
       B = StringBuffer('Hello W') 
       B.append('orld!') 
       print B.read(5) # 'Hello' 
       print B.read() # 'World!' 
  """ 
  
  def __init__(self, s=''): 
    Deque.__init__(self) 
    self.length = 0 
    self.append(s) 
    
  def append(self, s): 
    n = 128 
    for block in [s[i:i+n] for i in range(0,len(s),n)]: 
      self.push_last(block) 
    self.length += len(s) 
    
  def prepend(self, s): 
    n = 128 
    blocks = [s[i:i+n] for i in range(0,len(s),n)] 
    blocks.reverse() 
    for block in blocks: 
      self.push_first(block) 
    self.length += len(s) 
    
  def read(self, n=None): 
    if n == None or n > len(self): n = len(self) 
    destlen = len(self) - n 
    ans = [] 
    while len(self) > destlen: 
      ans += [self.pop_first()] 
      self.length -= len(ans[-1]) 
    ans = ''.join(ans) 
    self.prepend(ans[n:]) 
    ans = ans[:n] 
    return ans 
    
  def peek(self, n=None): 
    ans = self.read(n) 
    self.prepend(ans) 
    return ans 
    
  def __len__(self): return self.length 
  def __str__(self): return self.peek() 
  def __repr__(self): return 'StringBuffer(' + str(self) + ')'