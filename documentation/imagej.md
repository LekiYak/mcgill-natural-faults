# ImageJ 

1. Using an image editor, crop the scan so that the imprinted paper takes up the whole image.
2. Use a brush tool to paint all non-carbon-paper pixels of the image white. This includes the sample name, directional indicators, and of course dust and noise from the scanner.

! [Distiction between asperities and dust](https://i.imgur.com/0lvOWci.png "Distinction between asperities and dust")

3. Once the image has been cleaned, load it into ImageJ. Select `Process>Binary>Make Binary`. The image should invert colours so that the non-asperity portions are black.
4. Select `Analyze>Histogram`. A window should pop up. Select `List`. Only two colour values (0-Black and 255-White) should have corresponding counts. 
5. Copy down the counts corresponding to values 0 (Black) and 255 (White). Sum these count numbers to get the total number of pixels in your image.

$$\text{Total \# of pixels} = \text{Count}_{0} + \text{Count}_{255}$$

$$\text{Proportion of image that are asperities} = \frac{\text{Count}_{255}}{\text{Total \# of pixels}} =  \frac{\text{Count}_{255}}{\text{Count}_{0} + \text{Count}_{255}}$$


6. Once you know what proportion of your paper (image) is taken up by asperities, you can multiply this value by the dimensions of your paper (image) to get an estimate of the contact area. For example:

$$\text{Count}_{0} = 640000 \qquad \qquad\text{Count}_{255} = 18165$$

$$\text{Proportion of image that are asperities} =  \frac{\text{Count}_{255}}{\text{Count}_{0} + \text{Count}_{255}} = \frac{18165}{640000 + 18165}\approx 0.0276$$

The dimensions of letter size paper in mm are $215.9 \times 279.4$.

$$
\begin{align*}
\text{Asperity area} = \text{Paper area} \times \text{Asperity proportion} &= (215.9 \times 279.4) \times 0.0276 \\
&= 1665 \; \text{mm}^{2}


\end{align*}$$
