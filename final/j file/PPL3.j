.source PPL3.java
.class public PPL3
.super java/lang/Object
.implements Course

.field public number I

.method public <init>(I)V
  .limit stack 2
  .limit locals 2
  .line 4
  0: aload_0
  1: invokespecial java/lang/Object/<init>()V
  .line 5
  4: aload_0
  5: iload_1
  6: putfield PPL3/number I
  .line 6
  9: return
.end method

.method public study()V
  .limit stack 1
  .limit locals 1
  .line 10
  0: aload_0
  1: getfield PPL3/number I
  4: invokestatic io/putInt(I)V
  .line 11
  7: return
.end method


